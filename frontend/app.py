#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import os
import requests

from flask import Flask, Response
from flaskext.mysql import MySQL

app = Flask(__name__)


mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "skupper"
app.config["MYSQL_DATABASE_PASSWORD"] = "reppuks"
app.config["MYSQL_DATABASE_DB"] = "skupper"
app.config["MYSQL_DATABASE_HOST"] = "mydb"
app.config["MYSQL_DATABASE_PORT"] = 3306
mysql.init_app(app)


host = os.environ.get("FRONTEND_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("FRONTEND_SERVICE_PORT", 8080))


@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/")
def message():
    sql = "SELECT text FROM greetings where ID=1"
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as exception:
        data = str(exception)


    text = f"I am the frontend.  The database says '{data}'.\n"

    return Response(text, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host=host, port=port)
