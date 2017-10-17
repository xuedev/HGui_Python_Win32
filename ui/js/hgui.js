
//////////////////////////////////////////////////////////////////////////////////////////////
function Python(module, func, param) {
	top.ret = "";
    top.app.Python(module,func,param,function(data){
		top.ret = data;
	});
	return top.ret;
}

function PythonAsync(module, func, param, callback){
	top.app.PythonAsync(module,func,param,callback);
}
 /////////////////////////////////////////////数据库操作接口//////////////////////////////////////////////////////////
 function queryData(db_file,sql,callback){
	//RunAsync("DataAccess","QueryData",db_file+"@"+sql,callback);
	///**
	var param = {};
	param.file = "./data/"+db_file+".sdb";
	param.sql = sql;
	var str = JSON.stringify(param);

	PythonAsync("db","query",str,callback);
	//**/

}
//data的格式为 表名@列1@列2.....
function insertData(db_file,data,callback){
	//RunAsync("DataAccess","InsertData",db_file+"@"+data,callback);
	var param = {};
	param.file = "./data/"+db_file+".sdb";
	var arr = data.split("@");
	var values = "'"+arr[1]+"'";
	for(var i=2;i<arr.length;i++){
		values += ",'"+arr[i]+"'";
	}
	var sql = "INSERT INTO "+arr[0]+" VALUES ("+values+")";
	
	param.sql = sql;
	var str = JSON.stringify(param);
	PythonAsync("db","execute",str,callback);

}
function exeSql(db_file,sql,callback){
	//RunAsync("DataAccess","ExecuteSql",db_file+"@"+sql,callback);
	var param = {};
	param.file = "./data/"+db_file+".sdb";
	param.sql = sql;
	var str = JSON.stringify(param);

	PythonAsync("db","execute",str,callback);
}

var maxValue;
function queryMaxValue(db_file,table,callback){
	var param = {};
	param.file = "./data/"+db_file+".sdb";
	param.sql = "select max(id) as max from "+table;
	var str = JSON.stringify(param);

	PythonAsync("db","execute",str,function(data){
		var json = eval("("+data+")");
		maxValue = json[0].max;
		callback(maxValue);
	});

}
