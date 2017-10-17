
 function remove(){
	var _mask = document.getElementById('loading');    
    _mask.parentNode.removeChild(_mask);  
 }
 
 function init(){
	 var _html = "<div id='loading' style='position:absolute;left:0;width:100%;height:100%;top:0;background:#E0ECFF;opacity:0.8;filter:alpha(opacity=80);'>\   <div style='position:absolute;  cursor1:wait;left:40%;top:200px;width:auto;height:16px;padding:12px 5px 10px 30px;\    background:#fff;border:2px solid #ccc;color:#000;'>\正在加载，请等待...\</div></div>";    
	 document.write(_html); 

 }
  
 window.onload = function(){    
	
	//正式应用时，放开下面注释
	//remove();

	//测试效果，正式应用时用上面的语句
    setTimeout("remove();",2000);
 }        
 
init();