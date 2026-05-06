let pieChart;
let barChart;

async function refresh(){

 const r = await fetch('/api/stats');
 const d = await r.json();

 for(const key in d){
   const el = document.getElementById(key);
   if(el) el.innerText = d[key];
 }

 updateCharts(d);
}

function updateCharts(data){

 if(!pieChart){

 pieChart = new Chart(document.getElementById('pieChart'),{
   type:'pie',
   data:{
    labels:['CPU','Memory','Disk'],
    datasets:[{
      data:[data.cpu,data.memory,data.disk],
      backgroundColor:['#3b82f6','#22c55e','#f59e0b']
    }]
   }
 });

 barChart = new Chart(document.getElementById('barChart'),{
   type:'bar',
   data:{
    labels:['Upload','Download'],
    datasets:[{
      data:[data.network_sent,data.network_recv],
      backgroundColor:['#8b5cf6','#ef4444']
    }]
   }
 });

 return;
 }

 pieChart.data.datasets[0].data=[data.cpu,data.memory,data.disk];
 pieChart.update();

 barChart.data.datasets[0].data=[data.network_sent,data.network_recv];
 barChart.update();
}

refresh();
setInterval(refresh,2000);
