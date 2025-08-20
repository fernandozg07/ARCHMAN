import React from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Card, Text, Button, List, Divider } from 'react-native-paper';
import { useAuthStore } from '../../store/authStore';

export default function ProfileScreen({ navigation }: any) {
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    Alert.alert(
      'Sair',
      'Tem certeza que deseja sair?',
      [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Sair', onPress: logout, style: 'destructive' },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <Card style={styles.profileCard}>
        <Card.Content>
          <Text variant="headlineSmall" style={styles.name}>
            {user?.first_name} {user?.last_name}
          </Text>
          <Text variant="bodyMedium" style={styles.email}>
            {user?.email}
          </Text>
          <Text variant="bodySmall" style={styles.username}>
            @{user?.username}
          </Text>
        </Card.Content>
      </Card>

      <Card style={styles.menuCard}>
        <List.Item
          title="Editar Perfil"
          left={(props) => <List.Icon {...props} icon="account-edit" />}
          right={(props) => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => navigation.navigate('EditProfile')}
        />
        <Divider />
        <List.Item
          title="Configurações"
          left={(props) => <List.Icon {...props} icon="cog" />}
          right={(props) => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => {}}
        />
        <Divider />
        <List.Item
          title="Ajuda"
          left={(props) => <List.Icon {...props} icon="help-circle" />}
          right={(props) => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => {}}
        />
        <Divider />
        <List.Item
          title="Sobre"
          left={(props) => <List.Icon {...props} icon="information" />}
          right={(props) => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => {}}
        />
      </Card>

      <Button
        mode="outlined"
        onPress={handleLogout}
        style={styles.logoutButton}
        textColor="#D32F2F"
      >
        Sair
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 15,
  },
  profileCard: {
    marginBottom: 20,
    alignItems: 'center',
  },
  name: {
    textAlign: 'center',
    marginBottom: 5,
    color: '#2E7D32',
  },
  email: {
    textAlign: 'center',
    marginBottom: 5,
    color: '#666',
  },
  username: {
    textAlign: 'center',
    color: '#999',
  },
  menuCard: {
    marginBottom: 20,
  },
  logoutButton: {
    marginTop: 20,
    borderColor: '#D32F2F',
  },
});