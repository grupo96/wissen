import styled from "styled-components/native";

export const TextOne =  styled.Text`
    color:#000000;
    font-size: 20px;
    font-weight: 600;
    margin-bottom:60px;
    margin-top: 16px; 
`;

export const TextTwo =  styled.Text`
    color:#FFFFFF;
    font-size: 20px;
    font-weight: 600; 
`;
export const ContainerTipo = styled.View`
    background-color: #FFFFFF;
    width: 100%;
    align-items: center;
    max-width: 360px;
    height:445px;
    border-radius: 10px;
    padding: 20px;
`;

export const ButtonTipo = styled.TouchableOpacity`
    width:100%;
    background-color: #9DA983;
    max-width: 320px;
    height: 60px;
    flex-direction: row;
    justify-content: center;
    align-items:center;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 30px;
`;