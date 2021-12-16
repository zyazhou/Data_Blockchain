$(function(){
	$("#a1").click(function(){
		$("#template1").addClass("d-none");
		$(".right").addClass("d-none d-lg-block");
		$("#template2").removeClass("d-none");
	})
	
	$("#a2").click(function(){
		$("#template2").addClass("d-none");
		$(".right").addClass("d-none");
		$("#template1").removeClass("d-none");
	})
	
})

$(function(){
	$("#user_login").click(function(){
		$(".margin1").addClass("d-none");
		
		$(".margin3").removeClass("d-none");
	})
	
	$("#cancel").click(function(){
		$(".margin3").addClass("d-none");
		
		$(".margin1").removeClass("d-none");
	})
	
})

$(function(){
	$("#footer ul li").click(function(){
		$(this).find("a").addClass("ab");
		$(this).siblings().find("a").removeClass("ab");
	})
})

var app1=new Vue({
	el:"#app1",
	data:{
		username:"",
		passwd:"",
		info:""
	},
	methods:{

		login:function(){
			this.info=this.username;
			var that=this;
			var params = new URLSearchParams();
			params.append('username', this.username);
			params.append('passwd', this.passwd);
			axios.post("http://127.0.0.1:5000/user_login", params)
			/*axios.get("http://127.0.0.1:5000/user_login?username=this.username&passwd=this.passwd")*/
			/*axios.get("http://127.0.0.1:5000/user_login/"+this.username+'/'+this.passwd)*/
			.then(function(response){
				console.log(response.data)	
				alert('result:'+response.data['result'])
				$("#login_1").addClass("d-none");
				$(".login_2").removeClass("d-none");
				$(".login_figure").addClass("d-none");
				console.log("ok")
			},function(err){
				alert('error')
				console.log('no')
				})
		},


		showmore:function(){
			const  that=this;
			var i=0;
			var uername="";
			var password="";
			var money=0;
			var phone=0;
			var email=0;
			var params = new URLSearchParams();
			var dic = new Array();
			var lbt = "";
			params.append('username', this.username);
			axios.post("http://127.0.0.1:5000/showmore",params)
			.then(function(response){
				uername=response.data['username'];
				money=response.data['money'];
				phone=response.data['phone'];
				email=response.data['email'];
				console.log(uername)
				lbt += '<li><p>用户名：:'+uername+ ' </h6></li><li><h6>账户余额:'+money+' </h6></li><li><h6>手机号:'+phone+'</h6></li><li><h6>电子邮箱:'+email+'</h6></li>';
				$("#ul_class").removeClass("d-none");
				$("#ul_list1").empty();
				$("#ul_list1").append(lbt);
				console.log("ok")
			},function(err){

				console.log('no')
				})
		},
	},
	
})