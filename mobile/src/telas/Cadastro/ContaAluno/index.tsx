import { BackContainer, ContainerTwo, IconButton } from "../../styles";
import { Card, TextTitle, TextOne, TextTwo,  Input, ContainerForm, Button} from "../styles";
import { StackNavigationProp } from "@react-navigation/stack";
import { AntDesign } from "@expo/vector-icons"
import {Alert} from "react-native"

type Props = {
    navigation: StackNavigationProp<any>;
}

export default function ContaAluno({ navigation }: Props) {
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
                <TextTitle>Cadastrar Aluno</TextTitle>
                <TextOne>Nome Completo *</TextOne>
                <Input placeholder="Digite seu nome completo"></Input>
                <TextOne>E-mail *</TextOne>
                <Input placeholder="Digite seu e-mail"></Input>
                <TextOne>Senha *</TextOne>
                <Input placeholder="Digite sua senha"></Input>
                <TextOne>Número de telefone </TextOne>
                <Input placeholder="Digite seu número de telefone"></Input>
                <TextOne>Escola </TextOne>
                <Input placeholder="Digite o nome da escola"></Input>
                <TextOne>Série </TextOne>
                <Input placeholder="Digite a série que você cursa"></Input>
                <Button onPress={() => handleAviso()}>
                    <TextTwo>Cadastrar</TextTwo>
                </Button>
                </ContainerForm>
            </Card>
        </ContainerTwo>
    )
}