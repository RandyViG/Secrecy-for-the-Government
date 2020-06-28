/* Descifrar archivo con AES -> Todos los parámetros como cadena en hexadecimal*/
function decrypt_file(keys,nonce,file,filename,mime){
    var key = CryptoJS.enc.Base64.parse(keys);
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
function decrypt_RSAOAEP(data, key) {
    console.log(data)
    const privateKey = forge.pki.privateKeyFromPem(key);
    try {
        const t = privateKey.decrypt(forge.util.decode64(data), 'RSA-OAEP', {
            md: forge.md.sha1.create(),
                mgf1: {
                    md: forge.md.sha1.create()
                }
            });
            var h = window.btoa(t);
            return h
      } catch (error) {
        $("#errorRSA").modal();
      }
      
    

    return h
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
        console.log(key);
        var filename = $("#file_key").data("filename"); //Obtenemos el nombre del archivo a descargar
        console.log("Tenemos el archivo:"+filename)
        document.getElementById('file_key').setAttribute("data-filename", "");
        $.ajax({ //Solicitamos los datos del archivo a descargar
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: ($SCRIPT_ROOT + "/download"),
            data: JSON.stringify({file : filename}),
            success: function (data) {
                console.log("sucess");
                console.log("file:"+data.result["filename"]);
                h=decrypt_RSAOAEP(data.result["hash"],key); //Descifrar RSA OAEP
                decrypt_file(h,data.result["nonce"],data.result["file"],data.result["filename"],data.result["mime"]);
            },
            dataType: "json"
        });
    };
    lector.readAsText(archivo);
}

/*1.-Eventento principal, genera el input para la entrada de archivos y añade el EventListener*/
function recuperar(filename){
    $("#myModal").modal();
    document.getElementById('file_key').setAttribute("data-filename", filename);
    document.getElementById('file_key').addEventListener('change', leerArchivo, false);
    console.log("Listo para enviar:"+filename);
}
