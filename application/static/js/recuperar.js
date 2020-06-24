/* Descifrar archivo con AES -> Todos los parámetros como cadena en hexadecimal*/
function decrypt_file(keys,nonce,file,filename,mime){
    var key = CryptoJS.enc.Hex.parse(keys);
    var iv = CryptoJS.enc.Hex.parse(nonce+"000000000000000000000000000000000000000000000000");
    var texto = hexToBase64(file);
    var decrypted = CryptoJS.AES.decrypt(texto, key, {
        mode: CryptoJS.mode.CTR,
        iv: iv,
        padding: CryptoJS.pad.NoPadding
    });
    descargarArchivo(new Blob([_base64ToArrayBuffer(hexToBase64(decrypted.toString()))], { type: mime}),filename)
}

//Descifrar hash RSA OAEP
function decifrar_RSAOAEP(data, key) {
    console.log(data)
    const privateKey = forge.pki.privateKeyFromPem(key);
    const t = privateKey.decrypt(forge.util.decode64(data), 'RSA-OAEP', {
    md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });

    console.log(window.btoa(t));
    
}

/*2.-Obtenemos la información del archivo*/
function leerArchivo(e) {
    var archivo = e.target.files[0];
    var lector = new FileReader();
    lector.onload = function(e) {
        if( archivo.name.indexOf("pem") == -1 ){
            alert("Archivo inválido, intente de nuevo.");
            event.preventDefault();
            return;
        }
        var key = e.target.result;
        //key = (key.replace("-----BEGIN PRIVATE KEY-----\n","")).replace("\n-----END PRIVATE KEY-----","");
        console.log(key);
        var filename = $("#archivos_key").data("filename"); //Obtenemos el nombre del archivo a descargar
        console.log("Tenemos el archivo:"+filename)
        $('#get_key').css('background',"transparent");
        $("#get_key").empty(); //Quitamos el input generado del div
        $.ajax({ //Solicitamos los datos del archivo a descargar
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: ($SCRIPT_ROOT + "/download"),
            data: JSON.stringify({file : filename}),
            success: function (data) {
                console.log("sucess");
                console.log("file:"+data.result["filename"]);
                decifrar_RSAOAEP(data.result["hash"],key); //Descifrar RSA OAEP
                //decrypt_file(hash,data.result["nonce"],data.result["file"],data.result["filename"],data.result["mime"]);
            },
            dataType: "json"
        });
    };
    lector.readAsText(archivo);
}


/*1.-Eventento principal, genera el input para la entrada de archivos y añade el EventListener*/
function recuperar(filename){
    $("#get_key").append('<i style = "color: blue;float: left;font-family: Verdana;">'+ filename + '</i><input style = "float: left;" id = "archivos_key" type="file" name="file" data-filename="'+filename+'">');
    document.getElementById('archivos_key').addEventListener('change', leerArchivo, false);
    console.log("Listo para enviar:"+filename);
    alert("¡Ingresa tu llave privada!");
    event.preventDefault();
}