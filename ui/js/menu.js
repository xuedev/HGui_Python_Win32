//菜单回调函数
//////////////////////////////////////////////////////
function handleQueryMenu(data){
	try{
		var json = eval("("+data+")");
		for(var i=0;i<json.length;i++){
			var menu_parent = json[i].menu_parent;
			var menu_id = json[i].id;
			var menu_name = json[i].menu_name;
			if(menu_parent == "0"){
				top.addMainMenu(menu_id,menu_name);
			}
		}
		
		for(var i=0;i<json.length;i++){
			var menu_parent = json[i].menu_parent;
			var menu_id = json[i].id;
			var menu_name = json[i].menu_name;
			var menu_url = json[i].menu_url;
			if(menu_parent != "0"){
				top.addMenu(menu_parent,menu_name,menu_url,menu_id);
			}
		}

		$('#menus').accordion();
		

	}catch(e){
		alert(e);
		return;
	
	}
}

function handleQueryMenu_Update(data){
	//try{
		var frm = top.cdsz;
		if(frm != undefined){
			var json = eval("("+data+")");
			for(var i=0;i<json.length;i++){
				var menu_parent = json[i].menu_parent;
				var menu_id = json[i].id;
				var menu_name = json[i].menu_name;
				var position = json[i].position;
				var menu_url = json[i].menu_url;
				if(menu_parent == "0"){
					top.setMainMenu(menu_id,menu_name,menu_url,position);
				}
			}
			
			for(var i=0;i<json.length;i++){
				var menu_parent = json[i].menu_parent;
				var menu_id = json[i].id;
				var menu_name = json[i].menu_name;
				var menu_url = json[i].menu_url;
				var position = json[i].position;
				if(menu_parent != "0"){
					top.setMenu(menu_parent,menu_name,menu_url,menu_id,position);
				}
			}

			frm.applyUI();
		}
	//}catch(e){
	//	alert(e);
	//	return;
	
	//}
}
