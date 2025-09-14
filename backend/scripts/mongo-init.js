// Script de inicialización de MongoDB para el módulo de campañas

// Crear base de datos
db = db.getSiblingDB('inmax_campaigns');

// Crear colecciones con validación de esquemas
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["username", "email", "full_name", "hashed_password", "role", "status"],
      properties: {
        username: {
          bsonType: "string",
          minLength: 3,
          maxLength: 50,
          pattern: "^[a-zA-Z0-9_-]+$"
        },
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        full_name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        hashed_password: {
          bsonType: "string"
        },
        role: {
          bsonType: "string",
          enum: ["admin", "manager", "creator", "viewer"]
        },
        status: {
          bsonType: "string",
          enum: ["active", "inactive", "suspended", "pending"]
        },
        language: {
          bsonType: "string",
          enum: ["es", "en", "pt"]
        },
        timezone: {
          bsonType: "string"
        },
        created_at: {
          bsonType: "date"
        },
        updated_at: {
          bsonType: "date"
        },
        last_login: {
          bsonType: ["date", "null"]
        },
        is_verified: {
          bsonType: "bool"
        }
      }
    }
  }
});

db.createCollection('campaigns', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "budget", "start_date", "end_date", "user_id", "status"],
      properties: {
        name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 200
        },
        description: {
          bsonType: ["string", "null"],
          maxLength: 1000
        },
        budget: {
          bsonType: "number",
          minimum: 0
        },
        demographics: {
          bsonType: ["object", "null"]
        },
        channel: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        start_date: {
          bsonType: "date"
        },
        end_date: {
          bsonType: "date"
        },
        user_id: {
          bsonType: "objectId"
        },
        status: {
          bsonType: "string",
          enum: ["draft", "active", "paused", "finished", "cancelled"]
        },
        priority: {
          bsonType: "string",
          enum: ["low", "medium", "high", "urgent"]
        },
        target_locations: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["type", "coordinates"],
            properties: {
              type: {
                bsonType: "string",
                enum: ["point", "polygon", "circle", "country", "region"]
              },
              coordinates: {
                bsonType: "array",
                items: {
                  bsonType: "number"
                },
                minItems: 2,
                maxItems: 2
              },
              radius: {
                bsonType: ["number", "null"],
                minimum: 0
              },
              polygon_coordinates: {
                bsonType: ["array", "null"],
                items: {
                  bsonType: "array",
                  items: {
                    bsonType: "number"
                  },
                  minItems: 2,
                  maxItems: 2
                }
              },
              country: {
                bsonType: ["string", "null"]
              },
              region: {
                bsonType: ["string", "null"]
              },
              city: {
                bsonType: ["string", "null"]
              },
              address: {
                bsonType: ["string", "null"]
              }
            }
          }
        },
        media_files: {
          bsonType: "array",
          items: {
            bsonType: "objectId"
          }
        },
        created_at: {
          bsonType: "date"
        },
        updated_at: {
          bsonType: "date"
        },
        views_count: {
          bsonType: "int",
          minimum: 0
        },
        clicks_count: {
          bsonType: "int",
          minimum: 0
        },
        conversions_count: {
          bsonType: "int",
          minimum: 0
        }
      }
    }
  }
});

db.createCollection('media_files', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["filename", "original_filename", "file_type", "mime_type", "size", "url", "campaign_id", "user_id"],
      properties: {
        filename: {
          bsonType: "string",
          minLength: 1,
          maxLength: 255
        },
        original_filename: {
          bsonType: "string",
          minLength: 1,
          maxLength: 255
        },
        file_type: {
          bsonType: "string",
          enum: ["image", "video", "audio", "document"]
        },
        mime_type: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        size: {
          bsonType: "int",
          minimum: 1
        },
        url: {
          bsonType: "string"
        },
        thumbnail_url: {
          bsonType: ["string", "null"]
        },
        status: {
          bsonType: "string",
          enum: ["uploading", "processing", "ready", "error", "deleted"]
        },
        upload_date: {
          bsonType: "date"
        },
        processed_date: {
          bsonType: ["date", "null"]
        },
        campaign_id: {
          bsonType: "objectId"
        },
        user_id: {
          bsonType: "objectId"
        },
        error_message: {
          bsonType: ["string", "null"]
        },
        metadata: {
          bsonType: ["object", "null"]
        },
        image_metadata: {
          bsonType: ["object", "null"]
        },
        video_metadata: {
          bsonType: ["object", "null"]
        }
      }
    }
  }
});

db.createCollection('locations', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "coordinates"],
      properties: {
        name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 200
        },
        coordinates: {
          bsonType: "array",
          items: {
            bsonType: "number"
          },
          minItems: 2,
          maxItems: 2
        },
        country: {
          bsonType: ["string", "null"]
        },
        region: {
          bsonType: ["string", "null"]
        },
        city: {
          bsonType: ["string", "null"]
        },
        address: {
          bsonType: ["string", "null"]
        },
        place_type: {
          bsonType: ["array", "null"],
          items: {
            bsonType: "string"
          }
        },
        context: {
          bsonType: ["array", "null"],
          items: {
            bsonType: "object"
          }
        },
        relevance: {
          bsonType: ["number", "null"],
          minimum: 0,
          maximum: 1
        }
      }
    }
  }
});

// Crear índices para optimizar consultas
print("Creating indexes...");

// Índices para usuarios
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "role": 1 });
db.users.createIndex({ "status": 1 });
db.users.createIndex({ "created_at": -1 });

// Índices para campañas
db.campaigns.createIndex({ "user_id": 1 });
db.campaigns.createIndex({ "status": 1 });
db.campaigns.createIndex({ "start_date": 1 });
db.campaigns.createIndex({ "end_date": 1 });
db.campaigns.createIndex({ "created_at": -1 });
db.campaigns.createIndex({ "name": "text", "description": "text" }); // Índice de texto para búsqueda
db.campaigns.createIndex({ "target_locations": "2dsphere" }); // Índice geoespacial

// Índices para archivos multimedia
db.media_files.createIndex({ "campaign_id": 1 });
db.media_files.createIndex({ "user_id": 1 });
db.media_files.createIndex({ "file_type": 1 });
db.media_files.createIndex({ "status": 1 });
db.media_files.createIndex({ "upload_date": -1 });

// Índices para ubicaciones
db.locations.createIndex({ "coordinates": "2dsphere" }); // Índice geoespacial
db.locations.createIndex({ "name": 1 });
db.locations.createIndex({ "country": 1 });
db.locations.createIndex({ "region": 1 });
db.locations.createIndex({ "city": 1 });

print("Database initialization completed successfully!");
