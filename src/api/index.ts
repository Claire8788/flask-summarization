import request from '../utils/request';
import axios from 'axios';
// export const fetchData = () => {
//     return request({
//         url: 'https://www.fastmock.site/mock/dc695d037038802def4b989ba4650c3f/vms/getUser',
//         method: 'post'
//     });
// };

export const fetchData = (params) => {
    return request({
        url: 'http://127.0.0.1:5000/api/tableData',
        method: 'get',
        params: params // 将参数传递给后端
    });
};

// export const deleteData = (params) => {
//     return request({
//         url: 'http://127.0.0.1:5000/api/deleteData',
//         method: 'delete',
//         params: params // 将参数传递给后端
//     });
// };
export const deleteData = (params) => {
    return axios.delete('http://127.0.0.1:5000/api/deleteData', {
        data: params,
        headers: {
            'Content-Type': 'application/json'
        }
    });
};





export const queryUser = (params) => {
    return request({
        url: 'http://127.0.0.1:5000/api/queryUser',
        method: 'post',
        data: params // 将参数传递给后端
    });
};


export const deleteAdmin = (params) => {
    return axios.delete('http://127.0.0.1:5000/api/deleteAdmin', {
        data: params,
        headers: {
            'Content-Type': 'application/json'
        }
    });
};
