import axios from "axios";


const Get = async (url,token=null) => {

    const config = {
        headers: {
            'Authorization': `Token ${token}` // Добавляем токен в заголовок
        }
    }
    try {
        const res = await axios.get(url, token ? config: '' )

        return res
    }catch  (e){    
        console.log('Ошибка при' ,e);
        
    }

}


export default Get