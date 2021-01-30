let express           = require('express');
let app               = express();
let bodyParser        = require('body-parser');
let path              = require('path');
let http              = require('http');
let server            = http.createServer(app);
let spawn             = require('child_process').spawn;


app.use(express.json());
app.use(bodyParser.json());//accept json params
app.use(bodyParser.urlencoded({extended: true})); 
app.set('view engine', 'ejs');
app.engine('html',require('ejs').renderFile);

app.get('/',(request, response, next)=>{
    traitement(request, response);
});

app.post('/views/index.html', (request, response, next)=>{ 
    traitement(request, response);
});

function traitement(request, response){
    let datas = '';
    let process = spawn('python', ["./analyse_covid.py"]);
    //send to python
    let getContinent = request.body.continent;
    let getCountry = request.body.country;
    let beginDate = request.body.begin_date;
    let endDate = request.body.end_date;
    let today;
    if(beginDate == null || beginDate=="") today = new Date();
    else today = new Date(beginDate);
    let start = today.toDateString();
    beginDate = (today.getMonth()+1)+'/'+today.getDate()+'/'+today.getFullYear().toString().substring(2,4);

    if(endDate == null || endDate=="") today = new Date();
    else today = new Date(endDate);
    let end = today.toDateString();
    endDate = (today.getMonth()+1)+'/'+today.getDate()+'/'+today.getFullYear().toString().substring(2,4);

    let req = [getContinent, getCountry, beginDate, endDate];
    process.stdin.write(JSON.stringify(req));
    process.stdin.end();
    //Receive from python
    process.stdout.on('data', data =>{
        datas +=data.toString();
    });
    process.stdout.on('end', () =>{
        /*let result  = JSON.parse(datas);
        result['begin_date'] = start;
        result['end_date'] = end;
        let update = new Date(result['Last_Update'] );
        result['Last_Update'] = update.toDateString();
        //console.log(datas)*/
        response.render('index.html', {datan : datas});
    });
}
server.listen(8003);
