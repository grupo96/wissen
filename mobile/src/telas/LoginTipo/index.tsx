import { BackContainer, IconButton } from "../styles";
import {ContainerLogin, TextTitle, TextSubtitle, ButtonLogin, Input, ContainerForm, TextOne, TextTwo } from "./styles";
import { ContainerTwo } from "../styles";
import { AntDesign } from "@expo/vector-icons"
import { StackNavigationProp } from "@react-navigation/stack";
import {Alert} from "react-native"


type Props = {
    navigation: StackNavigationProp<any>;
}

export default function LoginTipo({ navigation }: Props) {
    const handleAviso = () => {
        Alert.alert("Ops!", "Essa opção não está disponivel no momento!",
        [
          { text: "Ok", style: "cancel" }
        ],
      )
    }
    return (
        <ContainerTwo>
            <ContainerLogin>
                <BackContainer>
                    <IconButton onPress={() => navigation.pop()}>
                        <AntDesign name="left" size={20} color="black" />
                    </IconButton>
                </BackContainer>
                <TextTitle>Login</TextTitle>
                <ContainerForm>
                    <TextOne>Email*</TextOne>
                    <Input></Input>
                    <TextOne>Senha*</TextOne>
                    <Input></Input>
                    <ButtonLogin  onPress={() => handleAviso()}>
                        <TextTwo>Login</TextTwo>
                    </ButtonLogin>
                </ContainerForm>
                <TextSubtitle onPress={() => handleAviso()}>Esqueci minha senha</TextSubtitle>
                <TextSubtitle onPress={() => navigation.navigate('criar-conta')}>Cadastre-se</TextSubtitle>
            </ContainerLogin>
        </ContainerTwo>
    )
}