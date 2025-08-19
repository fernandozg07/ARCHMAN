import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert, TextInput, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { apiService } from '../services/api';
import { theme } from '../styles/theme';

export default function RegisterScreen() {
  const navigation = useNavigation();
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
    phone: '',
    address: '',
    user_type: 'user' as 'user' | 'admin' | 'officer',
  });

  const handleRegister = async () => {
    if (!formData.email || !formData.password || !formData.first_name || !formData.last_name) {
      Alert.alert('Erro', 'Preencha os campos obrigatórios');
      return;
    }

    if (formData.password !== formData.password_confirm) {
      Alert.alert('Erro', 'As senhas não coincidem');
      return;
    }

    try {
      await apiService.register(formData);
      Alert.alert('Sucesso!', 'Conta criada com sucesso!', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao criar conta');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <View style={styles.logoContainer}>
            <Ionicons name="person-add" size={40} color={theme.colors.primary} />
          </View>
          <Text style={styles.title}>Criar Conta</Text>
          <Text style={styles.subtitle}>Preencha seus dados</Text>
        </View>

        <View style={styles.formCard}>
          <TextInput
            style={styles.input}
            placeholder="Nome *"
            placeholderTextColor="#a0a0a0"
            value={formData.first_name}
            onChangeText={(value) => setFormData(prev => ({ ...prev, first_name: value }))}
          />

          <TextInput
            style={styles.input}
            placeholder="Sobrenome *"
            placeholderTextColor="#a0a0a0"
            value={formData.last_name}
            onChangeText={(value) => setFormData(prev => ({ ...prev, last_name: value }))}
          />

          <TextInput
            style={styles.input}
            placeholder="Email *"
            placeholderTextColor="#a0a0a0"
            value={formData.email}
            onChangeText={(value) => setFormData(prev => ({ ...prev, email: value }))}
            keyboardType="email-address"
            autoCapitalize="none"
          />

          <TextInput
            style={styles.input}
            placeholder="Telefone"
            placeholderTextColor="#a0a0a0"
            value={formData.phone}
            onChangeText={(value) => setFormData(prev => ({ ...prev, phone: value }))}
          />

          <TextInput
            style={styles.input}
            placeholder="Endereço"
            placeholderTextColor="#a0a0a0"
            value={formData.address}
            onChangeText={(value) => setFormData(prev => ({ ...prev, address: value }))}
          />

          <TextInput
            style={styles.input}
            placeholder="Senha *"
            placeholderTextColor="#a0a0a0"
            value={formData.password}
            onChangeText={(value) => setFormData(prev => ({ ...prev, password: value }))}
            secureTextEntry
          />

          <TextInput
            style={styles.input}
            placeholder="Confirmar Senha *"
            placeholderTextColor="#a0a0a0"
            value={formData.password_confirm}
            onChangeText={(value) => setFormData(prev => ({ ...prev, password_confirm: value }))}
            secureTextEntry
          />

          <Text style={styles.label}>Tipo de Usuário</Text>
          <View style={styles.userTypeButtons}>
            {[
              { key: 'user', label: 'Usuário' },
              { key: 'admin', label: 'Admin' },
              { key: 'officer', label: 'Officer' }
            ].map((type) => (
              <TouchableOpacity
                key={type.key}
                style={[
                  styles.userTypeButton,
                  formData.user_type === type.key && styles.userTypeButtonActive
                ]}
                onPress={() => setFormData(prev => ({ ...prev, user_type: type.key as any }))}
              >
                <Text style={[
                  styles.userTypeButtonText,
                  formData.user_type === type.key && styles.userTypeButtonTextActive
                ]}>
                  {type.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <TouchableOpacity style={styles.button} onPress={handleRegister}>
            <Text style={styles.buttonText}>Criar Conta</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Text style={styles.linkText}>Já tem conta? Faça login</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    alignItems: 'center',
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    marginBottom: theme.spacing.lg,
  },
  logoContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: theme.colors.card,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: theme.colors.textSecondary,
  },
  formCard: {
    padding: theme.spacing.lg,
  },
  input: {
    backgroundColor: theme.colors.surface,
    padding: 15,
    borderRadius: theme.borderRadius.md,
    marginBottom: 15,
    fontSize: 16,
    color: theme.colors.text,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  button: {
    backgroundColor: theme.colors.primary,
    padding: 15,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
    marginTop: 10,
    shadowColor: theme.colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  linkText: {
    textAlign: 'center',
    color: theme.colors.primary,
    marginTop: 20,
    fontSize: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.primary,
    marginBottom: 8,
  },
  userTypeButtons: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 20,
  },
  userTypeButton: {
    flex: 1,
    padding: 12,
    borderRadius: theme.borderRadius.sm,
    backgroundColor: theme.colors.surface,
    borderWidth: 1,
    borderColor: theme.colors.border,
    alignItems: 'center',
  },
  userTypeButtonActive: {
    backgroundColor: theme.colors.primary,
    borderColor: theme.colors.primary,
  },
  userTypeButtonText: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    fontWeight: '500',
  },
  userTypeButtonTextActive: {
    color: 'white',
  },
});