(() =>{
function ab2str(buf) {
		return String.fromCharCode.apply(null, new Uint8Array(buf));
}

console.log("Generando llaves...");
window.crypto.subtle.generateKey({
	name: "RSA-OAEP",
	// Consider using a 4096-bit key for systems that require long-term security
	modulusLength: 2048,
	publicExponent: new Uint8Array([1, 0, 1]),
	hash: "SHA-256",
},
true,
["encrypt", "decrypt"]
).then(function(keyPair) {
	//const encryptButton = document.querySelector(".rsa-oaep .encrypt-button");
	//encryptButton.addEventListener("click", () => {
	window.crypto.subtle.exportKey(
		"pkcs8",
		keyPair.privateKey
	).then(function(exportedPrivateKey) {
		const exportedAsString=ab2str(exportedPrivateKey);
		const exportedAsBase64 = window.btoa(exportedAsString);
		const pemExported = `-----BEGIN PRIVATE KEY-----\n${exportedAsBase64}\n-----END PRIVATE KEY-----`;
		const encryptButton = document.querySelector("#foo\\:bar");
		encryptButton.addEventListener("click", () => {
			descargarArchivo(new Blob([pemExported], { type: 'application/x-pem-file'}),"privateKey.pem")
		});
		console.log(pemExported)
	})

	window.crypto.subtle.exportKey(
		"spki",
		keyPair.publicKey
	).then(function(exportedPublicKey) {
		const exportedAsString=ab2str(exportedPublicKey);
		const exportedAsBase64 = window.btoa(exportedAsString);
		const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;
		//descargarArchivo(new Blob([pemExported], { type: 'application/x-pem-file'}),"publicKey.pem")
		
		console.log(pemExported)
		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: ($SCRIPT_ROOT + "/auth/keygen"),
			data: JSON.stringify({k : exportedAsBase64}),
			success: function (data) {
			},
			dataType: "json"
		});
	});
});
//});
})();
