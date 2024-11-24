import { HeaderContainer, TextOne, TextTwo } from "./style";
import { StackNavigationProp } from "@react-navigation/stack";
import { BackContainer, IconButton } from "../styles";
import { AntDesign } from "@expo/vector-icons"

type Props = {
    navigation: StackNavigationProp<any>;
}
export default function Header({ navigation }: Props) {
    <HeaderContainer>
        <BackContainer>
            <IconButton onPress={() => navigation.pop()}>
                <AntDesign name="left" size={20} color="black" />
            </IconButton>
        </BackContainer>
        <TextOne>Iniciar Sessão</TextOne>
        <TextTwo>criar conta</TextTwo>
    </HeaderContainer>
}