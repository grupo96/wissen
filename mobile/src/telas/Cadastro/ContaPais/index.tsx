import { BackContainer, ContainerTwo, IconButton } from "../../styles";
import { Card, TextTitle, TextOne, TextTwo,  Input, ContainerForm, Button} from "../styles";
import { StackNavigationProp } from "@react-navigation/stack";
import { AntDesign } from "@expo/vector-icons"
import {Alert} from "react-native"

type Props = {
    navigation: StackNavigationProp<any>;
}

export default function ContaPais({ navigation }: Props) {
    const handleAviso = () => {
        Alert.alert("Ops!", "Essa opção não está disponível no momento!",
        [
          { text: "Ok", style: "cancel" }
        ],
      )
    }
    return (
        <ContainerTwo>
            <Card>
                <BackContainer>
                    <IconButton onPress={() => navigation.pop()}>
                        <AntDesign name="left" size={20} color="black" />
                    </IconButton>
                </BackContainer >
                <ContainerForm>
                <TextTitle>Cadastrar Pais</TextTitle>
                <TextOne>Nome Completo *</TextOne>
                <Input placeholder="Digite seu nome completo"></Input>
                <TextOne>E-mail *</TextOne>
                <Input placeholder="Digite seu e-mail"></Input>
                <TextOne>Senha *</TextOne>
                <Input placeholder="Digite sua senha"></Input>
                <TextOne>Nome do filho(a)</TextOne>
                <Input placeholder="Digite o nome do seu filho(a)"></Input>
                <Button onPress={() => handleAviso()}>
                    <TextTwo>Adicionar outro filho</TextTwo>
                </Button>
                <Button onPress={() => handleAviso()}>
                    <TextTwo>Cadastrar</TextTwo>
                </Button>
                </ContainerForm>
            </Card>
        </ContainerTwo>
    )
}