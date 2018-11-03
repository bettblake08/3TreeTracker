import BACK__11 from "../../images/back--11.jpg";
import MAIN_LOGO from "../../images/logo2.png";
import USER_50 from "../../images/user_50.jpg";
import USER_150 from "../../images/user_150.jpg";
import USER_200 from "../../images/user_200.jpg";

const WEB_URL = "http://localhost:5000/";
const SOCKET_URL = "ws://localhost:8080/";
const API_URL = `${WEB_URL}api/v1/`;

//let SOCKET_URL = "wss://900bbd6f.ngrok.io:8080/";
//let WEB_URL = "https://900bbd6f.ngrok.io/";

const DEFAULT_USER_PIC = [
    USER_50,
    USER_150,
    USER_200
];

const DEFAULT_PRODUCT_COVER_PIC = BACK__11;

const ADMIN_LOGIN_BACKGROUND = BACK__11;

export {
    WEB_URL,
    API_URL,
    SOCKET_URL,
    DEFAULT_PRODUCT_COVER_PIC,
    DEFAULT_USER_PIC,
    MAIN_LOGO
};