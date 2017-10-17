function stopEvent(e){
	if(e.pageY<35 && e.pageY>0)
				e.preventDefault()
}

$(function() {
		initTitleBar();
		$("#title").mousedown(function(e){
			app.sendMessage('mouse_down',[e.pageX,e.pageY]);
			stopEvent(e);
		});
		$("#title").mouseup(function(e){
			app.sendMessage('mouse_up',[e.pageX,e.pageY]);
			stopEvent(e);
			//e.preventDefault()
		});
		$("#title").mousemove(function(e){
			app.sendMessage('mouse_move',[e.pageX,e.pageY]);
			stopEvent(e);
			//e.preventDefault()
		});	

		$("#close").click(function(e){
			close();
		});
		$("#min").click(function(e){
			minimize();
		});
		$("#max").click(function(e){
			maximize();
		});

		$("#title").dblclick(function(e){
			maximize();
		});
	});


function initTitleBar(){
	var str= "<div id=\"title\" style=\"margin-left:auto;margin-right:auto;background:#5697D0;min-width:570px;;height:40px;\"><div id=\"text\" style=\"width:auto;height:35px;position:absolute;top:1px;left:10px;color:red;\"><h4></h4></div><div id=\"min\" style=\"background:url('assets/img/min_hover.png') no-repeat;width:35px;;height:35px;position:absolute;top:10px;right:70px;\"></div><div id=\"max\" style=\"background:url('assets/img/max_hover.png') no-repeat;width:35px;;height:35px;position:absolute;top:10px;right:35px;\"></div><div id=\"close\" style=\"background:url('assets/img/close_hover.png') no-repeat;width:35px;;height:35px;position:absolute;top:10px;right:0px;\"></div><div>";
	$("#myContent").before(str);
}

///**
window.alert = function(msg){
			$.messager.show({
					title:'提示',
					msg:msg
				});
		}
//**/

