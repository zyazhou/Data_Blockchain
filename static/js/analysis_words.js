var app=new Vue({
	el:".words_cloud",
	data:{
		keyword:"world_cloud01",
		png_name:""
	},
	methods:{
		search_keyword:function(){
			var that=this;
			
			console.log(this.keyword)
			axios.get("http://127.0.0.1:5000/analysis_words/"+this.keyword)
			.then(function(response){
				console.log("ok")
			},function(err){console.log(no)})
			


		},
		changeKey:function(key){
			
			this.keyword=key;
			
			this.png_name=key;
			this.search_keyword();
		},
		
		raise:function(key){
			var demo=document.getElementById("demo");
			var temp=this.keyword;
			var t='../static/images/scrapy_files/'+temp+'.png';
			demo.src=t
			demo.width="450";
			demo.height="450";
		}
	},
	
})

