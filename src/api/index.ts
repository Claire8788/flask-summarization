import request from '../utils/request';

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
