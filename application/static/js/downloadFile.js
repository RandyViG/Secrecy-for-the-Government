function descargarArchivo(contenidoEnBlob, nombreArchivo) {
    //creamos un FileReader para leer el Blob
    var reader = new FileReader();
    //Definimos la función que manejará el archivo
    //una vez haya terminado de leerlo
    reader.onload = function (event) {
        //Usaremos un link para iniciar la descarga 
        var save = document.createElement('a');
        save.href = event.target.result;
        save.target = '_blank';
        //Truco: así le damos el nombre al archivo 
        save.download = nombreArchivo || 'archivo.dat';
        var clicEvent = new MouseEvent('click', {
        'view': window,
        'bubbles': true,
        'cancelable': true
        });
        //Simulamos un clic del usuario
        //no es necesario agregar el link al DOM.
        save.dispatchEvent(clicEvent);
        //Y liberamos recursos...
        (window.URL || window.webkitURL).revokeObjectURL(save.href);
    };
    //Leemos el blob y esperamos a que dispare el evento "load"
    reader.readAsDataURL(contenidoEnBlob);
};