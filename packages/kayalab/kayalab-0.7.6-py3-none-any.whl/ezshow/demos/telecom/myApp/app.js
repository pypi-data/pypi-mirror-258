var createError = require("http-errors");
var express = require("express");
var fileUpload = require("express-fileupload");
var cors = require("cors");
var path = require("path");
var bodyParser = require("body-parser");
var cookieParser = require("cookie-parser");
var logger = require("morgan");

const config = require("./config");

var indexRouter = require("./routes/index");
var uploadRouter = require("./routes/upload");
var processRouter = require("./routes/process");
var modelRouter = require("./routes/model");
var graphdbRouter = require("./routes/graphdb");
var baseRouter = require("./routes/basedb");
var opentsdbRouter = require("./routes/opentsdb");

var app = express();
app.use(fileUpload());
app.use(cors());
app.set("views", path.join(__dirname, "views"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// view engine setup
app.set("view engine", "pug");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

app.use("/", indexRouter);
app.use("/upload", uploadRouter);
app.use("/process", processRouter);
app.use("/model", modelRouter);
app.use("/graphdb", graphdbRouter);
app.use("/basedb", baseRouter);
app.use("/opentsdb", opentsdbRouter);

// enable non-strict ssl
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render("error");
});

module.exports = app;
