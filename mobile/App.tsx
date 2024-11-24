import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import OnBoarding from './src/telas/OnBoarding';
import CriarConta from './src/telas/Cadastro/CriarConta';
import Login from './src/telas/Login';
import LoginTipo from './src/telas/LoginTipo';
import ContaAluno from './src/telas/Cadastro/ContaAluno';
import ContaProfessor from './src/telas/Cadastro/ContaProfessor';
import ContaPais from './src/telas/Cadastro/ContaPais';
import Header from './src/telas/Header';
import { createStackNavigator } from '@react-navigation/stack';

export default function App() {
  const Stack = createStackNavigator();
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="on-boarding" >
        <Stack.Screen name="on-boarding" component={OnBoarding} options={{ headerShown: false }} />
        <Stack.Screen name="criar-conta" component={CriarConta} options={{ headerShown: false }} />
        <Stack.Screen name="login" component={Login}  options={{ headerShown: false }}/>
        <Stack.Screen name="login-tipo" component={LoginTipo} options={{ headerShown: false }} />
        <Stack.Screen name="conta-aluno" component={ContaAluno} options={{ headerShown: false }} />
        <Stack.Screen name="conta-professor" component={ContaProfessor} options={{ headerShown: false }} />
        <Stack.Screen name="conta-pais" component={ContaPais} options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


