package com.example.myapplication

import android.app.Activity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.btn1).setOnClickListener {
            Toast.makeText(this, "Звук 1 выбран", Toast.LENGTH_SHORT).show()
        }

        findViewById<Button>(R.id.btn2).setOnClickListener {
            Toast.makeText(this, "Звук 2 выбран", Toast.LENGTH_SHORT).show()
        }

        findViewById<Button>(R.id.btn3).setOnClickListener {
            Toast.makeText(this, "Звук 3 выбран", Toast.LENGTH_SHORT).show()
        }

        findViewById<Button>(R.id.stop).setOnClickListener {
            Toast.makeText(this, "Стоп", Toast.LENGTH_SHORT).show()
        }
    }
}