from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/imagenes', methods=['GET'])
def obtener_imagenes():
    try:
        result = cloudinary.api.resources(
            type='upload',
            max_results=30 
        )

        return jsonify(result['resources'])
    except Exception as e:
        print(f'Error al obtener imágenes: {e}')
        return jsonify({'error': 'Error al obtener imágenes de Cloudinary'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)