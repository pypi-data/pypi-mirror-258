const config = {
  app: {
    port: 3002,
  },
  mapr: {
    opentsdb: "http://" + process.env.MAPR_CLUSTER + ":4242",
    gateway: "https://" + process.env.MAPR_CLUSTER + ":8047",
  },
};

module.exports = config;
