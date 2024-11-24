import styled from "styled-components/native";

export const Card = styled.View`
    flex: 1;
    background-color: #FFFFFF;
    width: 100%;
    align-items: center;
    max-width: 360px;
    border-radius: 10px;
    padding-horizontal: 20px;
    padding-top: 8px;
    margin-top: 8px;
`;

export const ContainerForm = styled.View`
    width: 100%;
    margin-top: 8px;
`;

export const TextTitle =  styled.Text`
    color:#000000;
    font-size: 20px;
    font-weight: 600;
    padding-bottom: 16px; 
    text-align: center;
`;

export const TextOne =  styled.Text`
    color:#000000;
    font-size: 18px;
    font-weight: 500; 
    text-align: left;
`;
export const Input = styled.TextInput`
  border:1px solid #989898;
  padding: 10px 10px;
  margin-bottom: 20px;
  font-size: 16px;
  margin-top: 8px;
  border-radius: 5px;
  height: 40px;
`;

export const TextTwo =  styled.Text`
    color:#FFFFFF;
    font-size: 18px;
    font-weight: 500;
`;

export const Button = styled.TouchableOpacity`
    width:100%;
    background-color: #9DA983;
    max-width: 320px;
    height: 60px;
    flex-direction: row;
    justify-content: center;
    align-items:center;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 32px;
    margin-bottom: 20px;
`;
