from numpy import load
from numpy import loadtxt
from base import readData
from numpy import nan
from numpy import isnan
from numpy import count_nonzero
from numpy import unique
from numpy import array
from sklearn.base import clone
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor


# split the dataset by 'chunkID', return a list of chunks
def to_chunks(values, chunk_ix=0):
    chunks = list()
    # get the unique chunk ids
    chunk_ids = unique(values[:, chunk_ix])
    # group rows by chunk id
    for chunk_id in chunk_ids:
        selection = values[:, chunk_ix] == chunk_id
        chunks.append(values[selection, :])
    return chunks


def split_train_test(chunks, row_in_chunk_ix=2):
    train, test = list(), list()
    # first 5 days of hourly observations for train
    cut_point = 5 * 24
    # enumerate chunks
    for k, rows in chunks.items():
        # split chunk rows by 'position_within_chunk'
        train_rows = rows[rows[:, row_in_chunk_ix] <= cut_point, :]
        test_rows = rows[rows[:, row_in_chunk_ix] > cut_point, :]
        if len(train_rows) == 0 or len(test_rows) == 0:
            print('>dropping chunk=%d: train=%s, test=%s' % (k, train_rows.shape, test_rows.shape))
            continue
        # store with chunk id, position in chunk, hour and all targets
        indices = [1, 2, 5] + [x for x in range(56, train_rows.shape[1])]
        train.append(train_rows[:, indices])
        test.append(test_rows[:, indices])
    return train, test


# return true if the array has any non-nan values
def has_data(data):
    return count_nonzero(isnan(data)) < len(data)


# return a list of relative forecast lead times
def get_lead_times():
    return [1, 2, 3, 4, 5, 10, 17, 24, 48, 72]


# fit a single model
def fit_model(model, X, y):
    # clone the model configuration
    local_model = clone(model)
    # fit the model
    local_model.fit(X, y)
    return local_model


# fit one model for each variable and each forecast lead time [var][time][model]
def fit_models(model, train):
    # prepare structure for saving models
    models = [[list() for _ in range(train.shape[1])] for _ in range(train.shape[0])]
    # enumerate vars
    for i in range(train.shape[0]):
        # enumerate lead times
        for j in range(train.shape[1]):
            # get data
            data = train[i, j]
            X, y = data[:, :-1], data[:, -1]
            # fit model
            local_model = fit_model(model, X, y)
            models[i][j].append(local_model)
    return models


# return forecasts as [chunks][var][time]
def make_predictions(models, test):
    lead_times = get_lead_times()
    predictions = list()
    # enumerate chunks
    for i in range(test.shape[0]):
        # enumerate variables
        chunk_predictions = list()
        for j in range(test.shape[1]):
            # get the input pattern for this chunk and target
            pattern = test[i, j]
            # assume a nan forecast
            forecasts = array([nan for _ in range(len(lead_times))])
            # check we can make a forecast
            if has_data(pattern):
                pattern = pattern.reshape((1, len(pattern)))
                # forecast each lead time
                forecasts = list()
                for k in range(len(lead_times)):
                    yhat = models[j][k][0].predict(pattern)
                    forecasts.append(yhat[0])
                forecasts = array(forecasts)
            # save forecasts for each lead time for this variable
            chunk_predictions.append(forecasts)
        # save forecasts for this chunk
        chunk_predictions = array(chunk_predictions)
        predictions.append(chunk_predictions)
    return array(predictions)


# convert the test dataset in chunks to [chunk][variable][time] format
def prepare_test_forecasts(test_chunks):
    predictions = list()
    # enumerate chunks to forecast
    for rows in test_chunks:
        # enumerate targets for chunk
        chunk_predictions = list()
        for j in range(3, rows.shape[1]):
            yhat = rows[:, j]
            chunk_predictions.append(yhat)
        chunk_predictions = array(chunk_predictions)
        predictions.append(chunk_predictions)
    return array(predictions)


# calculate the error between an actual and predicted value
def calculate_error(actual, predicted):
    # give the full actual value if predicted is nan
    if isnan(predicted):
        return abs(actual)
    # calculate abs difference
    return abs(actual - predicted)


# evaluate a forecast in the format [chunk][variable][time]
def evaluate_forecasts(predictions, testset):
    lead_times = get_lead_times()
    total_mae, times_mae = 0.0, [0.0 for _ in range(len(lead_times))]
    total_c, times_c = 0, [0 for _ in range(len(lead_times))]
    # enumerate test chunks
    for i in range(len(test_chunks)):
        # convert to forecasts
        actual = testset[i]
        predicted = predictions[i]
        # enumerate target variables
        for j in range(predicted.shape[0]):
            # enumerate lead times
            for k in range(len(lead_times)):
                # skip if actual in nan
                if isnan(actual[j, k]):
                    continue
                # calculate error
                error = calculate_error(actual[j, k], predicted[j, k])
                # update statistics
                total_mae += error
                times_mae[k] += error
                total_c += 1
                times_c[k] += 1
    # normalize summed absolute errors
    total_mae /= total_c
    times_mae = [times_mae[i] / times_c[i] for i in range(len(times_mae))]
    return total_mae, times_mae


# summarize scores
def summarize_error(name, total_mae):
    print('%s: %.3f MAE' % (name, total_mae))


# prepare a list of ml models
def get_models(models=dict()):
    # non-linear models
    models['knn'] = KNeighborsRegressor(n_neighbors=7)
    models['cart'] = DecisionTreeRegressor()
    models['extra'] = ExtraTreeRegressor()
    models['svmr'] = SVR()
    # # ensemble models
    n_trees = 100
    models['ada'] = AdaBoostRegressor(n_estimators=n_trees)
    models['bag'] = BaggingRegressor(n_estimators=n_trees)
    models['rf'] = RandomForestRegressor(n_estimators=n_trees)
    models['et'] = ExtraTreesRegressor(n_estimators=n_trees)
    models['gbm'] = GradientBoostingRegressor(n_estimators=n_trees)
    print('Defined %d models' % len(models))
    return models


# 模型评估
def evaluate_models(models, train, test, actual):
    for name, model in models.items():
        # 训练模型
        fits = fit_models(model, train)
        # make predictions
        predictions = make_predictions(fits, test)
        # evaluate forecast
        total_mae, _ = evaluate_forecasts(predictions, actual)
        # summarize forecast
        summarize_error(name, total_mae)


fileName = '../data/Y4_2022-07-01_tbl_pwrarrypwrcar1.csv'
dataset = readData(fileName=fileName)
# group data by chunks
values = dataset.values
chunks = to_chunks(values)
# split into train/test
train, test = split_train_test(chunks)

# # load supervised datasets
# train = load(r'E:\MyGit\BigDataFile\dsg-hackathon\supervised_train.npy', allow_pickle=True)
# test = load(r'E:\MyGit\BigDataFile\dsg-hackathon\supervised_test.npy', allow_pickle=True)
# print(train.shape, test.shape)
# # load test chunks for validation
# testset = loadtxt(r'E:\MyGit\BigDataFile\dsg-hackathon\naive_test.csv', delimiter=',')
# test_chunks = to_chunks(testset)
# actual = prepare_test_forecasts(test_chunks)
# # prepare list of models
# models = get_models()
# # evaluate models
# evaluate_models(models, train, test, actual)
