package com.ems.servlet;

import java.io.*;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;

import java.sql.*;

@WebServlet("/history")
public class HistoryServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        out.println("<h2>📊 Resume History</h2>");

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            Connection con = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/resume_db",
                    "root",
                    "1234"
            );

            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery("SELECT * FROM resumes");

            out.println("<table border='1' cellpadding='10'>");
            out.println("<tr><th>ID</th><th>File</th><th>Score</th><th>Suggestions</th><th>Date</th></tr>");

            while (rs.next()) {
                out.println("<tr>");
                out.println("<td>" + rs.getInt("id") + "</td>");
                out.println("<td>" + rs.getString("filename") + "</td>");
                out.println("<td>" + rs.getInt("score") + "</td>");
                out.println("<td>" + rs.getString("suggestions") + "</td>");
                out.println("<td>" + rs.getTimestamp("created_at") + "</td>");
                out.println("</tr>");
            }

            out.println("</table>");

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
            out.println("<p style='color:red;'>DB Error</p>");
        }
    }
}