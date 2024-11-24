import { useNavigation } from "@react-navigation/native"
import { ContainerLogo, ProjectName, ButtonOne,  ButtonTwo, TextOne, TextTwo, ContainerButton} from "./styles";
import { Image } from "react-native";
import { StackNavigationProp } from "@react-navigation/stack";
import { ContainerOne } from "../styles";

export default function OnBoarding() {
    const navigation = useNavigation<StackNavigationProp<any>>();

    return (
        <ContainerOne>
            <ContainerLogo>
                <Image source={require('../../../assets/img/logo.png')} />
                <ProjectName>Wissen</ProjectName>
            </ContainerLogo>
            <ContainerButton>
                <ButtonOne onPress={() => navigation.navigate('criar-conta')}>
                    <TextOne>Começar agora</TextOne>
                </ButtonOne>
                <ButtonTwo  onPress={() => navigation.navigate('login')}>
                    <TextTwo>Eu já tenho uma conta</TextTwo>
                </ButtonTwo>
            </ContainerButton>

        </ContainerOne>
    )
}