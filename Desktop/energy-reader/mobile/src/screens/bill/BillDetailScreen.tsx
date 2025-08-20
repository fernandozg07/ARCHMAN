import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Text, Chip, Button, Divider } from 'react-native-paper';

export default function BillDetailScreen({ route, navigation }: any) {
  const { bill } = route.params;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PROCESSED': return '#4CAF50';
      case 'PROCESSING': return '#FF9800';
      case 'FAILED': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.header}>
            <Text variant="headlineSmall">{bill.fornecedor || 'Conta de Energia'}</Text>
            <Chip 
              mode="flat" 
              textStyle={{ color: getStatusColor(bill.status) }}
              style={{ backgroundColor: `${getStatusColor(bill.status)}20` }}
            >
              {bill.status === 'PROCESSED' ? 'Processado' : bill.status}
            </Chip>
          </View>

          <View style={styles.section}>
            <Text variant="titleMedium" style={styles.sectionTitle}>Consumo e Valores</Text>
            
            <View style={styles.row}>
              <Text style={styles.label}>Consumo:</Text>
              <Text style={styles.valueHighlight}>
                {bill.consumo_kwh ? `${bill.consumo_kwh} kWh` : 'N/A'}
              </Text>
            </View>

            <View style={styles.row}>
              <Text style={styles.label}>Valor Total:</Text>
              <Text style={styles.valueHighlight}>
                {bill.valor_total ? `R$ ${parseFloat(bill.valor_total).toFixed(2)}` : 'N/A'}
              </Text>
            </View>

            <View style={styles.row}>
              <Text style={styles.label}>Cliente:</Text>
              <Text style={styles.value}>{bill.numero_cliente || 'N/A'}</Text>
            </View>

            <View style={styles.row}>
              <Text style={styles.label}>Período:</Text>
              <Text style={styles.value}>
                {bill.period_start && bill.period_end 
                  ? `${new Date(bill.period_start).toLocaleDateString('pt-BR')} - ${new Date(bill.period_end).toLocaleDateString('pt-BR')}`
                  : 'N/A'
                }
              </Text>
            </View>
          </View>
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
    marginBottom: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  section: {
    marginVertical: 10,
  },
  sectionTitle: {
    marginBottom: 15,
    color: '#2E7D32',
    fontWeight: 'bold',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  label: {
    flex: 1,
    color: '#666',
    fontWeight: '500',
  },
  value: {
    flex: 1,
    textAlign: 'right',
    color: '#333',
  },
  valueHighlight: {
    flex: 1,
    textAlign: 'right',
    color: '#2E7D32',
    fontWeight: 'bold',
    fontSize: 16,
  },
});