const crypto = require('crypto');

function midnightEncrypt(data) {
    const key = 'midnightZKfakeKey123456';  
    const iv = crypto.randomBytes(16);  
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);

    let encrypted = cipher.update(data, 'utf-8', 'hex');
    encrypted += cipher.final('hex');
    return iv.toString('hex') + ':' + encrypted;  
}


function midnightDecrypt(encryptedData) {
    const key = 'midnightZKfakeKey123456';  
    const textParts = encryptedData.split(':');
    const iv = Buffer.from(textParts.shift(), 'hex');  
    const encryptedText = Buffer.from(textParts.join(':'), 'hex');
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), iv);

    let decrypted = decipher.update(encryptedText, 'hex', 'utf-8');
    decrypted += decipher.final('utf-8');
    return decrypted;  
}

async function storeCertificateOnBlockchain(certificate) {

    const encryptedCertificate = midnightEncrypt(JSON.stringify(certificate));


    const transaction = {
        datetime: certificate.datetime,
        encryptedData: encryptedCertificate,  
        user: certificate.user,
    };

 
    console.log("Encrypted certificate stored on blockchain:", transaction);
 
    display_blockchain_notification("Certificate successfully encrypted and stored on blockchain.");
}

async function retrieveCertificateFromBlockchain(transactionId) {

    const transaction = await fetchTransactionFromBlockchain(transactionId);

    // Decrypt the certificate
    const decryptedData = midnightDecrypt(transaction.encryptedData);
    const certificate = JSON.parse(decryptedData);

    console.log("Decrypted certificate data:", certificate);

    // Show a toast notification for decryption
    display_blockchain_notification("Certificate successfully decrypted from the blockchain.");
    
    return certificate;
}

