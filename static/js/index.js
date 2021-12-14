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
	
	},
	
})

	    var app=new Vue({
	    el:"#app2",
		data:{
			items:[]
		},
		methods:{
			show:function(){
				axios.post("http://127.0.0.1:5000/search_blockchain")
				.then(function(response){
						console.log(response.data)	;
						alert('yes');
						this.items.shift();
						console.log("ok");
					},function(err){
						alert('error');
						console.log('no');
						})
				},
			}
		}
	    })