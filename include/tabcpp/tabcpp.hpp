/*
 * Copyright (c) Matthew Smith (DeltaBoyBZ)
 * Provided under an MIT license as part of the tabular-cpp project
 * found at https://github.com/DeltaBoyBZ/tabular-cpp 
 */

#pragma once

#include<iostream>
#include<vector>
#include<map>
#include<cstring>
#include<limits>

// the main struct defining a table
#define TABCPP_TABLE(name, keytype, constructor, destructor, field_declarations, add_func, remove_func)\
    class name : public tabcpp::Table<keytype> {\
        public:\
                constructor\
                destructor\
                field_declarations\
                add_func\
                remove_func\
    };\
                
#define TABCPP_CONSTRUCTOR(tablename, fieldname, keytype)\
    tablename(){\
        this->key = &this->fieldname;\
        std::numeric_limits<keytype> lim;\
        this->keyMax = lim.max();\
    }

#define TABCPP_DESTRUCTOR(tablename)\
    ~tablename(){\
    }

// a table field (column) represented by a std::vector<type>
#define TABCPP_FIELD(keytype, type, name)\
    tabcpp::Table<keytype>::TableField<type> name = tabcpp::Table<keytype>::TableField<type>(this);


// the function which takes the elements of a row and appends said row to the table
// with a manual key
#define TABCPP_ADD_FUNC_MAN(keytype, args, update)\
    void add(args){\
        update\
        this->indices.insert(std::pair<keytype, int>(*this->key->rbegin(), this->key->size() - 1));\
    }

// the function which takes the elements of a row and appends said row to the table
// with an automatic key 
#define TABCPP_ADD_FUNC_AUTO(keytype, args, update)\
    int add(args){\
        update\
        int keyval;\
        if(this->key->empty()) keyval = 0;\
        else if(!full){\
            keyval = *(this->key->rbegin()) + 1;\
            if(keyval >= keyMax) full = true;\
        }\
        else if(!this->reserve.empty()) {\
            keyval = this->reserve.back();\
            this->reserve.pop_back();\
        }\
        else return -1;\
        this->key->push_back(keyval);\
        this->indices.insert(std::pair<keytype, int>(keyval, this->key->size() - 1));\
        return keyval;\
    }

// the function which removes a row from a table, given the row key
#define TABCPP_REMOVE_FUNC(keytype, update)\
    void remove(keytype id) override {\
        int index = 0;\
        for(keytype keyval : *this->key){\
            if(keyval == id) break;\
            index++;\
        }\
        if(index == this->key->size()) return;\
        update\
        this->reserve.push_back(index);\
        this->indicesCurrent = false;\
    }

// appending a field vector
#define TABCPP_APPEND(field, val)\
    this->field.push_back(val);\

// erasing from a field vector
#define TABCPP_REMOVE(field, index)\
    this->field.erase(this->field.begin() + index);
        
// wrapper for function arguments
#define TABCPP_ARGS(...) __VA_ARGS__

// declaration of a handle
#define TABCPP_HANDLE(type, member)\
    type member; 


namespace tabcpp
{
    template <typename KeyType>
    class Table
    {
        
        public:
            template <typename FieldType>
            class TableField : public std::vector<FieldType>
            {
                public:
                    TableField(Table<KeyType>* parent): parent(parent) {
                        this->clear();
                    };

                    template <typename T>
                    FieldType get(T val)
                    {
                        return get(parent->labels[val]);
                    } 


                    FieldType get(KeyType keyval)
                    {
                        if(!parent->indicesCurrent) parent->remap();
                        int index = parent->indices[keyval];         
                        return this->at(index);
                    }


                    FieldType* getPtr(KeyType keyval)
                    {
                        if(!parent->indicesCurrent) parent->remap();
                        int index = parent->indices[keyval];
                        return &this->at(index);
                    }

                    void set(KeyType keyval, FieldType fieldval)
                    {
                        if(!parent->indicesCurrent) parent->remap();
                        int index = parent->indices[keyval];
                        this->at(index) = fieldval;
                    }

                    KeyType findFirst(FieldType fieldval)
                    {
                        KeyType keyval = -1;
                        for(long i = 0; i < parent->key->size(); i++)
                        {
                            if((*this)[i] == fieldval)
                            {
                                keyval = parent->key->at(i);
                                break;
                            }
                        }
                        return keyval;
                    }

                    std::vector<KeyType> findAll(FieldType fieldval)
                    {
                        std::vector<KeyType> keyvals = {};
                        for(long i = 0; i < parent->key->size(); i++)
                        {
                            if((*this)[i] == fieldval) keyvals.push_back(parent->key->at(i));
                        } 
                        return keyvals;
                    }

                    std::map<FieldType, KeyType> createKeyMap(std::vector<KeyType> keyrange)
                    {
                        std::map<FieldType, KeyType> keyMap; 
                        for(KeyType keyval : keyrange)
                        {
                            FieldType fieldval = this->get(keyval); 
                            keyMap.insert(std::pair<FieldType, KeyType>(fieldval, keyval));
                        }
                        return keyMap;
                    }

                private:
                    Table<KeyType>* parent;
            };
            std::vector<KeyType>* key; 
            std::map<std::string, KeyType> labels;
            std::map<std::string, void*> vals;
            std::map<KeyType, int> indices;
            std::vector<KeyType> reserve = {}; 
            bool indicesCurrent = true;
            bool full = false;
            KeyType keyMax; 
    

            virtual ~Table() {}

            virtual void remove(KeyType keyval) {};

            void makeLabel(KeyType keyval, std::string name)
            {
                this->labels.insert(std::pair<std::string, KeyType>(name, keyval));    
            }             

            void remap()
            {
                for(long i = 0; i < this->key->size(); i++)
                {
                    this->indices[key->at(i)] = i;
                }
                this->indicesCurrent = true;
            }

            void clear()
            {
                while(!this->key->empty()) this->remove(*this->key->begin());
                full = false;
            }

            template <typename ValType>
            void createVal(std::string name, ValType val)
            {
                ValType* valptr = new ValType;
                *valptr = val;
                this->vals.insert(std::pair<std::string, void*>(name, valptr));
            } 

            template <typename ValType>
            void setVal(std::string name, ValType val)
            {
                *((ValType*)this->vals[name]) = val;
            }

            template <typename ValType>
            ValType getVal(std::string name)
            {
                return *((ValType*)this->vals[name]);
            }

            void destroyVal(std::string name)
            {
                delete this->vals[name];
                this->vals.erase(name);
            }
    };
}

