module.exports = {
  networks: {
    development: {
      host: "127.0.0.1", // Ganache default host
      port: 7545,        // Ganache default port
      network_id: "*",   // Match garne to any network 
    },
  },
  compilers: {
    solc: {
      version: "0.8.17",  // Use the appropriate Solidity version
    },
  },
};
