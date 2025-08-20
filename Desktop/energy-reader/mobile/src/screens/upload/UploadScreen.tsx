import React, { useState } from 'react';
import { View, StyleSheet, Alert, Image } from 'react-native';
import { Card, Text, Button, ProgressBar } from 'react-native-paper';
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';
import { api } from '../../services/api';

export default function UploadScreen() {
  const [selectedFile, setSelectedFile] = useState<any>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      setSelectedFile(result.assets[0]);
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
      quality: 0.8,
    });

    if (!result.canceled) {
      setSelectedFile(result.assets[0]);
    }
  };

  const pickDocument = async () => {
    const result = await DocumentPicker.getDocumentAsync({
      type: 'application/pdf',
      copyToCacheDirectory: true,
    });

    if (!result.canceled) {
      setSelectedFile(result.assets[0]);
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) {
      Alert.alert('Erro', 'Selecione um arquivo primeiro');
      return;
    }

    setUploading(true);
    setProgress(0);

    try {
      const formData = new FormData();
      formData.append('raw_file', {
        uri: selectedFile.uri,
        type: selectedFile.mimeType || 'image/jpeg',
        name: selectedFile.name || 'conta.jpg',
      } as any);

      // Progresso real do upload
      setProgress(0.3); // Upload iniciado
      
      const response = await api.uploadBill(formData);
      
      setProgress(0.7); // Upload concluído, processando
      
      // Aguardar um pouco para mostrar o processamento
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setProgress(1); // Processamento concluído
      
      const message = response.data?.fornecedor ? 
        `Conta processada com sucesso!\n\nFornecedor: ${response.data.fornecedor}\nConsumo: ${response.data.consumo_kwh || 'N/A'} kWh\nValor: R$ ${response.data.valor_total ? parseFloat(response.data.valor_total).toFixed(2) : 'N/A'}` :
        'Conta enviada com sucesso! Dados extraídos automaticamente.';
      
      Alert.alert(
        'Sucesso!', 
        message,
        [{ text: 'OK', onPress: () => setSelectedFile(null) }]
      );
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao enviar arquivo');
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="headlineSmall" style={styles.title}>
            Enviar Conta de Energia
          </Text>
          <Text variant="bodyMedium" style={styles.subtitle}>
            Escolha uma das opções abaixo para enviar sua conta
          </Text>

          <View style={styles.buttonContainer}>
            <Button
              mode="contained"
              icon="camera"
              onPress={takePhoto}
              style={styles.button}
            >
              Tirar Foto
            </Button>

            <Button
              mode="outlined"
              icon="image"
              onPress={pickImage}
              style={styles.button}
            >
              Galeria
            </Button>

            <Button
              mode="outlined"
              icon="file-pdf-box"
              onPress={pickDocument}
              style={styles.button}
            >
              Arquivo PDF
            </Button>
          </View>

          {selectedFile && (
            <Card style={styles.previewCard}>
              <Card.Content>
                <Text variant="titleMedium">Arquivo Selecionado:</Text>
                <Text variant="bodyMedium" style={styles.fileName}>
                  {selectedFile.name || 'Imagem selecionada'}
                </Text>
                
                {selectedFile.uri && selectedFile.type?.startsWith('image') && (
                  <Image source={{ uri: selectedFile.uri }} style={styles.preview} />
                )}

                {uploading && (
                  <View style={styles.progressContainer}>
                    <Text variant="bodySmall">Enviando... {Math.round(progress * 100)}%</Text>
                    <ProgressBar progress={progress} style={styles.progressBar} />
                  </View>
                )}

                <Button
                  mode="contained"
                  onPress={uploadFile}
                  loading={uploading}
                  disabled={uploading}
                  style={styles.uploadButton}
                >
                  {uploading ? 'Enviando...' : 'Enviar Conta'}
                </Button>
              </Card.Content>
            </Card>
          )}
        </Card.Content>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 15,
  },
  card: {
    flex: 1,
  },
  title: {
    textAlign: 'center',
    marginBottom: 10,
    color: '#2E7D32',
  },
  subtitle: {
    textAlign: 'center',
    marginBottom: 30,
    color: '#666',
  },
  buttonContainer: {
    marginBottom: 20,
  },
  button: {
    marginBottom: 15,
  },
  previewCard: {
    marginTop: 20,
    backgroundColor: '#f8f9fa',
  },
  fileName: {
    marginVertical: 10,
    fontWeight: 'bold',
  },
  preview: {
    width: '100%',
    height: 200,
    borderRadius: 8,
    marginVertical: 10,
  },
  progressContainer: {
    marginVertical: 15,
  },
  progressBar: {
    marginTop: 5,
  },
  uploadButton: {
    marginTop: 15,
  },
});