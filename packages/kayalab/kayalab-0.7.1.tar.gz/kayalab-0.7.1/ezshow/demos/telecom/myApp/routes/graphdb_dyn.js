var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var fetch = require('node-fetch')
var app = express()
var jsonParser = bodyParser.json()
const https = require('https');


const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});

router.post('/', jsonParser, function(req, res, next) {

   const input = req.body;
   console.log(input);

   const table = input.table
   const action = input.action;
   const nodeid = input.nodeid;

   let url =  'https://vm-ynsect-poc.sf5mmyfzh2qutoin3joinwdoch.parx.internal.cloudapp.net:8243/api/v2/table';
//   let url = 'http://localhost:3011/data';

   try {

        var response = { "nodes" : [], "edges": [] };

        switch (action) {
        case "viewnode":

                        call(url + '/%2Fynsect%2Fnodes/document/' + nodeid)
                                .then( data => {
                                        response.nodes.push(data);
                                        res.json(response);
                                });
                        break;
                case "viewchild":

                        call(url + '//%2Fynsect%2Fedges?condition={"$eq":{"source":"' + nodeid + '"}}' )
                                .then( data => {
                                        response.edges = data.DocumentStream;
                                        const nodeids = response.edges.map( d => '"'+ d.target +'"');
                                        console.log(url + '/%2Fynsect%2Fnodes?condition={"$in":{"_id":[' + nodeids.toString() + ']}}');

                                        call( url + '/%2Fynsect%2Fnodes?condition={"$in":{"_id":[' + nodeids.toString() + ']}}' )
                                                .then( data1 => {
                                                        response.nodes = data1.DocumentStream;
                                                        console.log(response.nodes)
                                                        res.json(response);
                                                })
                                })
                        break;
                default:
                        console.log("action not defined: " + action)
        }

   } catch (err) {
     console.log(err);
     res.status(500).send(err);
   }
});


async function call(url) {

         result = await fetch(url, {
            method: 'GET',
            agent: httpsAgent,
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Basic ' + Buffer.from('mapr:HPE25#31invent!').toString('base64')
            }
        })
        .then( (data) => { return data.json(); } )
        .catch(err => console.error(err));

    return result;
}



module.exports = router;
