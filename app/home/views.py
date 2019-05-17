import os

import simplejson
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import ExtraTreesClassifier

from werkzeug import secure_filename
from flask import request, render_template, redirect, url_for

from . import home
from .. import db
from .utils import UploadFile, DataFrameImputer
from ..models import Result


UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
IGNORED_FILES = set(['.gitignore'])

names = [
    "Nearest Neighbors",
    "Linear SVM",
    "RBF SVM",
    "Gaussian Process",
    "Decision Tree",
    "Random Forest",
    "Neural Net",
    "AdaBoost",
    "Naive Bayes",
    "QDA"
]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()
]


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    i = 1
    while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


@home.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = UploadFile(
                    name=filename,
                    type=mime_type,
                    size=0,
                    not_allowed_msg="File type not allowed"
                )

            else:
                # save file to disk
                uploaded_file_path = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
                files.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = UploadFile(name=filename, type=mime_type, size=size)

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [
            f
            for f in os.listdir(UPLOAD_FOLDER)
            if (
                os.path.isfile(os.path.join(UPLOAD_FOLDER, f)) and
                f not in IGNORED_FILES
            )
        ]

        file_display = []

        for f in files:
            size = os.path.getsize(
                os.path.join(UPLOAD_FOLDER, f)
            )
            file_saved = UploadFile(name=f, size=size)
            file_display.append(file_saved.get_file())
        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@home.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        Result.query.filter_by(file_name=filename).delete()
        db.session.commit()
        return simplejson.dumps({filename: 'True'})


@home.route("/analyze/<string:filename>", methods=['GET'])
def analyze(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        results = Result.query.with_entities(
            Result.company_name,
            Result.attr1, Result.ratio1,
            Result.attr2, Result.ratio2,
            Result.attr3, Result.ratio3,
            Result.algo1
        ).filter_by(file_name=filename)

        if results.count() == 0:
            results = []
            extension = filename.rsplit('.', 1)[1].lower()

            # read file
            if extension == 'csv':
                df = pd.read_csv(file_path)
            else:
                # TODO
                # read xls format file
                pass

      
            df = DataFrameImputer().fit_transform(df)

            # Encoding categorical data
            y = df.iloc[:, 0].values
            X = df.iloc[:, 1:]

            # covert categorical data using pandas
            categorical_columns = [key for key in dict(X.dtypes) if dict(X.dtypes)[key] not in ['float64', 'int64']]
            for column in categorical_columns:
                X[column] = X[column].astype('category')
                X[column] = X[column].cat.codes

            labelencoder_y = LabelEncoder()
            y = labelencoder_y.fit_transform(y)

            model = ExtraTreesClassifier()
            model.fit(X, y)
            importances = model.feature_importances_
            indices = np.argsort(importances)
            result = Result(
                company_name=filename,
                file_name=filename,
                attr1=X.columns[indices[-1]],
                ratio1=float(importances[indices[-1]]) * 100,
                attr2=X.columns[indices[-2]],
                ratio2=float(importances[indices[-2]]) * 100,
                attr3=X.columns[indices[-3]],
                ratio3=float(importances[indices[-3]]) * 100,
                algo1 ="Logistic Regression"
            )
            db.session.add(result)
            results.append(result)
            db.session.commit()

        return render_template(
            'home/analyze.html', filename=filename, results=results
        )

    else:
        return render_template("errors/404.html")


@home.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')
