import { AntDesign } from "@expo/vector-icons"
import { ContainerTipo, TextOne, TextTwo, ButtonTipo } from "./styles";
import { BackContainer, ContainerTwo, IconButton } from "../../styles";
import { StackNavigationProp } from "@react-navigation/stack";
import {Alert} from "react-native"

type Props = {
    navigation: StackNavigationProp<any>;
}

export default function CriarConta({ navigation }: Props) {
    const handleAviso = () => {
        Alert.alert("Ops!", "Essa opção estará disponível em breve!",
        [
          { text: "Ok", style: "cancel" }
        ],
      )
    }
    return (
        <ContainerTwo>
            <ContainerTipo>
                <BackContainer>
                    <IconButton onPress={() => navigation.pop()}>
                        <AntDesign name="left" size={20} color="black" />
                    </IconButton>
                </BackContainer >
                <TextOne>Selecione o tipo de cadastro</TextOne>
                <ButtonTipo onPress={() => navigation.navigate('conta-aluno')}>
                    <TextTwo>Aluno</TextTwo>
                </ButtonTipo>
                <ButtonTipo onPress={() => navigation.navigate('conta-professor')}>
                    <TextTwo>Professor</TextTwo>
                </ButtonTipo>
                <ButtonTipo onPress={() => navigation.navigate('conta-pais')}>
                    <TextTwo>Pais</TextTwo>
                </ButtonTipo>
            </ContainerTipo>
        </ContainerTwo>
    )
}
