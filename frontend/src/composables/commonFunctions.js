import { ref } from "vue";

const CommonFunctions = () => {

    const dateFormat = (inputDate, format) => {
        if(inputDate == '' || inputDate == null){
            return ''
        }
        const date = new Date(inputDate);
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();    
        format = format.replace("MM", month.toString().padStart(2,"0"));        
        if (format.indexOf("yyyy") > -1) {
            format = format.replace("yyyy", year.toString());
        }else if (format.indexOf("yy") > -1) {
            format = format.replace("yy", year.toString().substr(2,2));
        }
        format = format.replace("dd", day.toString().padStart(2,"0"));
        return format;
    };

    const formatBytes = (bytes, decimals = 2) => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const dm = decimals < 0 ? 0 : decimals
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
    };

    const trimString = (string) => {
        return string.trim()
    };

    const exportDataToCSV = (ref) => {
        ref.exportCSV();
    };

    function isFileImage(fileName) {
        const images = ['jpg', 'png', 'jpeg', 'webp']
        const ext = fileName.substring(fileName.lastIndexOf('.') + 1, fileName.length) || fileName
        return images.includes(ext.toLowerCase())
    }

    function capitalizeFirstLetters(string) {
        return string.replace(/(^\w{1})|(\s+\w{1})/g, letter => letter.toUpperCase())
    }

    function truncateString(str, n){
        return (str.length > n) ? str.slice(0, n-1) + '...' : str;
    }

    return {
        dateFormat,
        formatBytes,
        trimString,
        isFileImage,
        capitalizeFirstLetters,
        truncateString,
        exportDataToCSV
    };
};

export default CommonFunctions;
