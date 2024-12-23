import { io } from 'socket.io-client';

// "undefined" means the URL will be computed from the `window.location` object
const URL = 'https://flask-backend-1043469906200.asia-east1.run.app';

export const socket = io(URL);
