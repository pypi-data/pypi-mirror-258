var express = require("express");
var router = express.Router();
var bodyParser = require("body-parser");
var fetch = require("node-fetch");
var makeFetchCookie = require("fetch-cookie");

var app = express();
var jsonParser = bodyParser.json();
const https = require("https");
const config = require("../config");

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});

function getBaseStation(input) {
  const timestamp = input.timestamp || 1401617220;
  const timeExp =
    "A.startime < " + timestamp + " and A.endtime >= " + timestamp;

  const selection = input.selection;
  const latitudes = [selection[0][0], selection[1][0]];
  const longitudes = [selection[0][1], selection[1][1]];
  const latExp =
    "latitude between " +
    Math.min(...latitudes) +
    " and " +
    Math.max(...latitudes);
  const longExp =
    "longitude between " +
    Math.min(...longitudes) +
    " and " +
    Math.max(...longitudes);

  return (
    "select A.base as base, B.latitude as latitude, B.longitude as longitude, count(*) as total   from dfs.`/telecom/calls` as A, dfs.`/telecom/basestations` as B where A.base = B.id and " +
    timeExp +
    " group by base, latitude, longitude"
  );
}

const cookieJar = new makeFetchCookie.toughCookie.CookieJar(undefined, {
  allowSpecialUseDomain: true,
});

//const fetchCookie = makeFetchCookie(fetch,cookieJar)

function getSessionId() {
  fetchCookie(config.mapr.gateway + "/j_security_check", {
    method: "POST",
    body:
      "j_username=" +
      app.get("MAPR_USER") +
      "&j_password=" +
      app.get("MAPR_PASS"),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  }).then((data) => {
    //       console.log(cookieJar.toJSON())
  });
}

router.post("/", jsonParser, function (req, res, next) {
  const input = req.body;
  const maxRows = input.limit || 0;
  const query = getBaseStation(input);

  //  console.log( query);

  fetchCookie = makeFetchCookie(fetch, cookieJar);
  fetchCookie(config.mapr.gateway + "/j_security_check", {
    method: "POST",
    body:
      "j_username=" +
      app.get("MAPR_USER") +
      "&j_password=" +
      app.get("MAPR_PASS"),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  }).then((data) => {
    //          console.log(cookieJar.toJSON())

    try {
      fetchCookie(config.mapr.gateway + "/query.json", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          queryType: "SQL",
          autoLimit: maxRows,
          query: query,
          userName: app.get("MAPR_USER"),
        }),
        agent: httpsAgent,
      })
        .then((data) => {
          //			      console.log(data)
          return data.json();
        })
        .then((data) => {
          res.json(data);
        });
    } catch (err) {
      console.log(err);
      res.status(500).send(err);
    }
  });
});

module.exports = router;
