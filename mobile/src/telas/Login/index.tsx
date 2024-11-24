import { ContainerTexto, TextTitle, TextSubtitle, ContainerImagem, ContainerButton, ButtonOne, ButtonTwo, TextOne, TextTwo, TextThree, HeaderContainer, TextFour, ContainerIniciar} from "./styles";
import { ContainerOne, BackContainer, IconButton } from "../styles";
import { Image } from "react-native";
import { StackNavigationProp } from "@react-navigation/stack";
import { Alert } from "react-native"
import { AntDesign } from "@expo/vector-icons"

type Props = {
    navigation: StackNavigationProp<any>;
}

export default function Login({ navigation }: Props) {
    const handleAviso = () => {
        Alert.alert("Ops!", "Essa opção não está disponivel no momento!",
            [
                { text: "Ok", style: "cancel" }
            ],
        )
    }
    return (
        <ContainerOne>
            <HeaderContainer>
                <ContainerIniciar>
                    <BackContainer>
                        <IconButton onPress={() => navigation.pop()}>
                            <AntDesign name="left" size={20} color="black" />
                        </IconButton>
                        <TextFour onPress={() => navigation.navigate('login-tipo')}>Iniciar sessão</TextFour>
                    </BackContainer>
                </ContainerIniciar>
                <TextThree onPress={() => navigation.navigate('criar-conta')}>criar conta</TextThree>
            </HeaderContainer>
            <ContainerTexto>
                <TextTitle>Bem-vindo novamente!</TextTitle>
                <TextSubtitle>Há muitas atividades a espera para serem resolvidas por você</TextSubtitle>
            </ContainerTexto>
            <ContainerImagem>
                <Image source={require('../../../assets/img/college-students.png')} />
            </ContainerImagem>
            <ContainerButton>
                <ButtonOne onPress={() => handleAviso()}>
                    <Image source={require('../../../assets/img/google-icon.png')} />
                    <TextOne>Continuar com Google</TextOne>
                </ButtonOne>
                <ButtonTwo onPress={() => navigation.navigate('login-tipo')}>
                    <TextTwo>Continuar com E-mail</TextTwo>
                </ButtonTwo>
            </ContainerButton>
        </ContainerOne>
    )
}