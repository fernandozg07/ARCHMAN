import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { useNavigation } from '@react-navigation/native';
import { theme } from '../styles/theme';

export default function CameraScreen() {
  const navigation = useNavigation();
  const [isProcessing, setIsProcessing] = useState(false);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      processImage();
    }
  };

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Erro', 'Permissão de câmera necessária');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      processImage();
    }
  };

  const processImage = async () => {
    setIsProcessing(true);
    
    // Simular processamento
    setTimeout(() => {
      setIsProcessing(false);
      Alert.alert(
        'Processamento Concluído!',
        'Conta processada com sucesso!\n\nFornecedor: Enel\nConsumo: 150 kWh\nValor: R$ 125,50',
        [
          { text: 'Ver Dashboard', onPress: () => navigation.navigate('Dashboard' as never) },
          { text: 'OK' }
        ]
      );
    }, 3000);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <Ionicons name="camera" size={80} color={theme.colors.primary} />
          <Text style={styles.title}>Fotografar Conta</Text>
          <Text style={styles.subtitle}>
            Tire uma foto da sua conta de energia para processamento automático
          </Text>
        </View>

        <View style={styles.actions}>
          <TouchableOpacity 
            style={[styles.actionButton, styles.cameraButton]}
            onPress={takePhoto}
            disabled={isProcessing}
          >
            <Ionicons name="camera" size={32} color="white" />
            <Text style={styles.actionButtonText}>Tirar Foto</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={[styles.actionButton, styles.galleryButton]}
            onPress={pickImage}
            disabled={isProcessing}
          >
            <Ionicons name="images" size={32} color="white" />
            <Text style={styles.actionButtonText}>Escolher da Galeria</Text>
          </TouchableOpacity>
        </View>

        {isProcessing && (
          <View style={styles.processingContainer}>
            <Ionicons name="sync" size={40} color={theme.colors.primary} />
            <Text style={styles.processingText}>Processando imagem...</Text>
            <Text style={styles.processingSubtext}>
              Extraindo dados da conta de energia
            </Text>
          </View>
        )}

        <View style={styles.tips}>
          <Text style={styles.tipsTitle}>💡 Dicas para melhor resultado:</Text>
          <Text style={styles.tipText}>• Certifique-se de que a conta está bem iluminada</Text>
          <Text style={styles.tipText}>• Mantenha a câmera estável</Text>
          <Text style={styles.tipText}>• Capture toda a conta na foto</Text>
          <Text style={styles.tipText}>• Evite reflexos e sombras</Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  content: {
    flex: 1,
    padding: theme.spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginTop: 20,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  actions: {
    gap: 16,
    marginBottom: 40,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    borderRadius: theme.borderRadius.lg,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  cameraButton: {
    backgroundColor: theme.colors.primary,
    shadowColor: theme.colors.primary,
  },
  galleryButton: {
    backgroundColor: '#2196F3',
    shadowColor: '#2196F3',
  },
  actionButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 12,
  },
  processingContainer: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.lg,
    marginBottom: 30,
  },
  processingText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginTop: 16,
  },
  processingSubtext: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    marginTop: 8,
  },
  tips: {
    backgroundColor: theme.colors.surface,
    padding: 20,
    borderRadius: theme.borderRadius.lg,
  },
  tipsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: 12,
  },
  tipText: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    marginBottom: 8,
    lineHeight: 20,
  },
});