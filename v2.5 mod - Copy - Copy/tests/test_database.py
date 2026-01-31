"""
Tests para la funcionalidad de base de datos
TODO: Implementar tests unitarios
"""

import unittest
import sqlite3
import os
import sys

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestDatabase(unittest.TestCase):
    """Tests para la base de datos"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.test_db = 'test_inventario.db'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_creation(self):
        """Test: Verificar que la base de datos se crea correctamente"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Crear tabla de prueba
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
        self.assertTrue(os.path.exists(self.test_db))
    
    # TODO: Agregar más tests
    # - Test de inserción de piezas
    # - Test de inserción de vehículos
    # - Test de consultas
    # - Test de eliminación


if __name__ == '__main__':
    unittest.main()

