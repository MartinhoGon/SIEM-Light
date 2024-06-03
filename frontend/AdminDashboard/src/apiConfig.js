const API_BASE_URL = "http://127.0.0.1:8000/api"

const endpoints = {
    getHelper: `${API_BASE_URL}/helper/1/`,
    startListener: `${API_BASE_URL}/start-listener/`,
    stopListener: `${API_BASE_URL}/stop-listener/`,
    startSniffer: `${API_BASE_URL}/start-sniffer/`,
    stopSniffer: `${API_BASE_URL}/stop-sniffer/`,
    getStats: `${API_BASE_URL}/get-stats/`,
    feeds: `${API_BASE_URL}/feed/`,
    alertEndpoint: `${API_BASE_URL}/alert/`,
    fileUpload: `${API_BASE_URL}/upload-file/`,
    getInterfaces: `${API_BASE_URL}/network-interfaces/`,

}

export default endpoints;