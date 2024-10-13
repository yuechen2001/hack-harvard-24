const crypto = require('crypto');

function midnightEncrypt(data) {
    const key = 'midnightZKfakeKey123456';  // Hardcoded secret key
    const iv = crypto.randomBytes(16);  // Generate initialization vector
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);

    let encrypted = cipher.update(data, 'utf-8', 'hex');
    encrypted += cipher.final('hex');
    return iv.toString('hex') + ':' + encrypted;  // Combine IV and encrypted data
}


function midnightDecrypt(encryptedData) {
    const key = 'midnightZKfakeKey123456';  // Same secret key as for encryption
    const textParts = encryptedData.split(':');
    const iv = Buffer.from(textParts.shift(), 'hex');  // Extract IV
    const encryptedText = Buffer.from(textParts.join(':'), 'hex');
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), iv);

    let decrypted = decipher.update(encryptedText, 'hex', 'utf-8');
    decrypted += decipher.final('utf-8');
    return decrypted;  // Return decrypted data
}

async function storeCertificateOnBlockchain(certificate) {
    // Step 1: Encrypt certificate data
    const encryptedCertificate = midnightEncrypt(JSON.stringify(certificate));

    // Step 2: Store encrypted certificate on blockchain
    const transaction = {
        datetime: certificate.datetime,
        encryptedData: encryptedCertificate,  // Store the encrypted data
        user: certificate.user,
    };

    // Simulate blockchain store logic here
    console.log("Encrypted certificate stored on blockchain:", transaction);
    
    // Show a toast notification on the UI for encryption
    display_blockchain_notification("Certificate successfully encrypted and stored on blockchain.");
}

async function retrieveCertificateFromBlockchain(transactionId) {
    // Simulate fetching encrypted certificate from blockchain
    const transaction = await fetchTransactionFromBlockchain(transactionId);

    // Decrypt the certificate
    const decryptedData = midnightDecrypt(transaction.encryptedData);
    const certificate = JSON.parse(decryptedData);

    console.log("Decrypted certificate data:", certificate);

    // Show a toast notification for decryption
    display_blockchain_notification("Certificate successfully decrypted from the blockchain.");
    
    return certificate;
}

