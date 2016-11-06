setInterval(function getData(){
  peticion();
}, 120000);


function pintarMarca(data){
     var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: new google.maps.LatLng(42.8169, -1.6432),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    var infowindow = new google.maps.InfoWindow();

   var markers = [];
    for(var i=0; i< data.length; i++) {
        var parking = new Object();
        parking = data[i][0];
        var color_icon;
        
        if(parking.estado == 'bajo'){
            color_icon=new google.maps.MarkerImage('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
        }
        if(parking.estado=='medio'){
            color_icon= new google.maps.MarkerImage('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png');
        }
        if(parking.estado=='alto'){
            color_icon= new google.maps.MarkerImage('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
        }
        markers[i] = new google.maps.Marker({
            position: {lat:parseFloat(parking.latitud), lng:parseFloat(parking.longitud)},
            map: map,
            html: '<div id="contentInfoWindow" class="contentMap"><div class="contentTxt">Parking '+parking.nombre +' : '+parking.porcentaje +'</div></div>',
            id: parking.codigo,
            icon:color_icon,
    });
      
    google.maps.event.addListener(markers[i], 'click', function(){
      var infowindow = new google.maps.InfoWindow({
        id: this.id,
        content:this.html,
        position:this.getPosition(),
      });
      google.maps.event.addListenerOnce(infowindow, 'closeclick', function(){
        markers[this.id].setVisible(true);
      });
      this.setVisible(false);
      infowindow.open(map);
    });
    }   
}
document.addEventListener("DOMContentLoaded", function(){
    peticion();
});

function peticion(){
    var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
        console.log(xhttp.responseText);
        var data = JSON.parse(xhttp.responseText);
        pintarMarca(data);
    }
  };
  xhttp.open("GET", "/data", true);
  xhttp.send(); 
 
}
