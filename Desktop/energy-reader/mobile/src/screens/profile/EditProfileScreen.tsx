import React, { useState } from 'react';
import { View, StyleSheet, Alert, ScrollView } from 'react-native';
import { TextInput, Button, Card } from 'react-native-paper';
import { useAuthStore } from '../../store/authStore';
import { api } from '../../services/api';

export default function EditProfileScreen({ navigation }: any) {
  const { user, login } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    phone: user?.phone || '',
  });

  const handleSave = async () => {
    setLoading(true);
    try {
      const updatedUser = await api.updateProfile(formData);
      
      // Atualizar store local
      if (user) {
        const newUser = { ...user, ...updatedUser };
        await login(user.accessToken || '', user.refreshToken || '', newUser);
      }
      
      Alert.alert('Sucesso', 'Perfil atualizado com sucesso!', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao atualizar perfil');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <TextInput
            label="Nome"
            value={formData.first_name}
            onChangeText={(text) => setFormData(prev => ({ ...prev, first_name: text }))}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Sobrenome"
            value={formData.last_name}
            onChangeText={(text) => setFormData(prev => ({ ...prev, last_name: text }))}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Email"
            value={formData.email}
            onChangeText={(text) => setFormData(prev => ({ ...prev, email: text }))}
            mode="outlined"
            keyboardType="email-address"
            style={styles.input}
          />

          <TextInput
            label="Telefone"
            value={formData.phone}
            onChangeText={(text) => setFormData(prev => ({ ...prev, phone: text }))}
            mode="outlined"
            keyboardType="phone-pad"
            style={styles.input}
          />

          <Button
            mode="contained"
            onPress={handleSave}
            loading={loading}
            style={styles.button}
          >
            Salvar Alterações
          </Button>

          <Button
            mode="outlined"
            onPress={() => navigation.goBack()}
            style={styles.button}
          >
            Cancelar
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 15,
  },
  card: {
    marginTop: 20,
  },
  input: {
    marginBottom: 15,
  },
  button: {
    marginBottom: 10,
  },
});