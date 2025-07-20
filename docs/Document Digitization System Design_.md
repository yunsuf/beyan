

# **System Design Document: Project Digitize \- An Agentic Framework for Intelligent Document Processing**

## **Executive Summary**

### **Purpose**

This document presents a comprehensive system design for an advanced, agentic Intelligent Document Processing (IDP) system, codenamed "Project Digitize." The system is engineered to automate the extraction and integration of data from diverse business documents, thereby replacing the current manual data entry workflow. The objective is to provide a detailed architectural blueprint that serves as the foundation for the development, deployment, and evolution of a scalable, accurate, and intelligent automation solution.

### **Problem Statement**

The organization currently relies on a manual data entry process to digitize information from critical business documents, such as commercial invoices and packing lists. This manual approach is inherently slow, costly, and susceptible to human error, creating operational bottlenecks and compromising data integrity. The significant variation in document layouts and formats, as seen in examples from different suppliers like Samsung and Janssen 1, renders traditional, template-based automation methods ineffective and brittle. The challenge is to create a unified system that can intelligently handle this variability, scale with a "huge database" of existing records, and integrate seamlessly with a complex ecosystem of existing APIs for data validation and updates.

### **Proposed Solution**

The proposed solution is a hierarchical multi-agent system (MAS) that orchestrates a team of specialized AI agents to perform the end-to-end document processing workflow. This architecture is designed for modularity, scalability, and resilience. The cognitive core of the system will be a state-of-the-art, layout-aware Large Language Model (LLM), chosen for its superior ability to understand and extract data from complex, unstructured, and variable document formats without relying on rigid templates.

This core extraction capability is supported by a robust, multi-stage validation framework to ensure data accuracy, a Human-in-the-Loop (HITL) subsystem to manage exceptions and provide quality assurance, and a continual learning mechanism that uses human feedback to systematically improve model performance over time. The entire workflow is managed by a durable orchestration engine, ensuring reliable execution of long-running, asynchronous processes.

### **Key Benefits**

The implementation of Project Digitize will yield transformative benefits, aligning with the established advantages of modern IDP solutions.2 The system is projected to:

* **Increase Efficiency and Reduce Costs:** By automating repetitive data entry, the system will dramatically lower the per-document processing cost and time, freeing human operators to focus on higher-value, strategic activities.2  
* **Enhance Data Accuracy:** The combination of intelligent extraction, automated validation rules, and targeted human review will significantly reduce the error rates associated with manual entry, leading to more reliable data in downstream systems.4  
* **Improve Scalability and Flexibility:** The agent-based, cloud-native architecture is designed to handle fluctuating document volumes on demand. It can be easily extended to support new document types with minimal redevelopment effort, providing a future-proof platform for business growth.7  
* **Accelerate Business Processes:** Faster document processing will reduce turnaround times for critical functions like accounts payable, logistics, and inventory management, overcoming existing bottlenecks.5

### **Structure of this Document**

This document provides a detailed technical blueprint for Project Digitize. It begins with the high-level system architecture, followed by a deep dive into the specific roles, responsibilities, and technologies of each AI agent. Subsequent sections detail the operational workflow, the critical Human-in-the-Loop subsystem, data modeling and integration strategies, and a long-term roadmap for system scalability, reliability, and continuous improvement.

---

## **Section 1: High-Level System Architecture**

This section establishes the foundational architectural philosophy for Project Digitize. It justifies the selection of a multi-agent framework as the most effective approach for tackling the complexities of the task and presents a visual blueprint of the entire process, setting the stage for the detailed component analysis that follows.

### **1.1 The Rationale for an Agentic Framework in IDP**

The challenge of processing a high volume of documents with diverse layouts necessitates an architecture that is inherently flexible, robust, and maintainable. A single, monolithic application, while seemingly simpler to conceptualize, would quickly become a bottleneck. Such a system would be brittle, with any change or failure in one part of the logic risking the entire process. It would be difficult to update, maintain, and scale, particularly as new document formats are introduced. The user's request for an "agentic system" is a strategically sound starting point that directly addresses these challenges.

A multi-agent system (MAS) is an architecture composed of multiple autonomous, intelligent agents that interact with each other within a shared environment to achieve a common goal.7 This design paradigm is analogous to modern software engineering principles like microservices, where a large, complex problem is decomposed into smaller, specialized, and more manageable sub-problems.7 Adopting a MAS approach for Project Digitize provides several decisive advantages:

* **Specialization and Enhanced Problem-Solving:** Each agent is designed to be an expert in a specific domain. For instance, one agent specializes in image pre-processing, another in data extraction, and a third in data validation. This division of labor allows for the use of the best-suited technology for each sub-task, leading to a form of "collective intelligence" that is more powerful than a single, general-purpose system.7  
* **Scalability and Flexibility:** The agents are decoupled components. This means they can be developed, deployed, and scaled independently. During periods of high document influx, the system can dynamically increase the number of Extraction Agents to handle the load without impacting the performance of the Ingestion or Validation Agents. This elasticity is a critical requirement for supporting the existing "huge database" and future growth.7  
* **Resilience and Fault Tolerance:** As a distributed system, the MAS is inherently more resilient. The failure of a single agent does not necessarily halt the entire system. Workflows can be designed with robust error-handling mechanisms, such as automated retries for an individual agent's task, ensuring that transient issues do not cause catastrophic failures.7  
* **Maintainability and Evolvability:** The modular nature of the MAS simplifies the development and maintenance lifecycle. An individual agent can be updated, improved, or even completely replaced with a new technology without requiring a full system redeployment. This makes the system easier to adapt to future business needs and technological advancements.

### **1.2 Proposed Architectural Pattern: A Hierarchical Agent Orchestra with a Temporal Conductor**

While the autonomy of agents is a key strength, their activities must be carefully coordinated to ensure the correct sequence of operations and the integrity of the end-to-end process. Uncoordinated agents would result in process chaos. To solve this, the proposed architecture employs a hierarchical model featuring a master "Orchestrator" agent that directs a team of subordinate, specialized agents.7 This pattern provides the ideal balance of centralized control over the business workflow and delegated, specialized execution of individual tasks.

The Orchestrator's role is not to perform the tasks itself, but to act as a "conductor" for the agentic orchestra. It is responsible for managing the state of each document's workflow, invoking the correct subordinate agent at the appropriate time, ensuring seamless handoffs of data between agents, and managing the overall process from initial ingestion to final integration.9

Rather than building this complex orchestration logic from scratch, the design recommends leveraging a dedicated, durable workflow orchestration engine such as Temporal. Temporal is explicitly designed to manage stateful, long-running, and asynchronous workflows, which is a perfect technological match for this multi-agent process.9 It provides enterprise-grade features out-of-the-box, including:

* **State Management:** Reliably maintains the state of every document workflow, even over long periods (e.g., if a document is pending human review for days).  
* **Task Queuing and Retries:** Automatically manages task queues for each agent and handles transient failures with configurable retry policies.  
* **Visibility and Auditing:** Provides a clear view into the status of every workflow, offering a complete audit trail of the process.

This architectural choice—separating the "what to do next" (workflow logic in the Orchestrator) from the "how to do it" (task execution in the agents)—is fundamental. It means the business process can be modified within the Orchestrator without redeploying the agents, and an agent's internal technology can be upgraded without altering the workflow logic. This decoupling dramatically enhances the system's long-term flexibility and maintainability.

### **1.3 System Blueprint: End-to-End Document Flow**

The following diagram provides a high-level blueprint of the entire system, illustrating the journey of a document as it moves through the various agents. It visualizes the primary success path as well as key exception paths, such as the Human-in-the-Loop review cycle.

Kod snippet'i

graph TD  
    subgraph "Input Sources"  
        A\[Email Inbox\]  
        B  
        C\[API Endpoint\]  
    end

    subgraph "Project Digitize: Agentic System"  
        D\[Ingestion Agent\] \--\> E{Orchestrator (Temporal)};  
        E \-- 1\. Start Workflow \--\> F\[Pre-processing & Classification Agent\];  
        F \-- 2\. Classified Doc \--\> E;  
        E \-- 3\. Route for Extraction \--\> G\[Extraction Agent \- Layout-Aware LLM\];  
        G \-- 4\. Extracted JSON \--\> E;  
        E \-- 5\. Route for Validation \--\> H\[Validation Agent\];  
        H \-- 6\. Validation Result \--\> E;  
        E \-- 7\. Check Confidence \--\> I{Confidence Gate};  
        I \-- High Confidence / STP \--\> J\[Integration Agent\];  
        I \-- Low Confidence / Validation Fail \--\> K;  
        K \-- Corrected Data \--\> L\[Learning Agent\];  
        L \-- Updated Model \--\> G;  
        K \-- Approved Data \--\> J;  
        J \-- 8\. Final API Call \--\> M;  
    end

    subgraph "External Systems"  
        H \--\> N;  
        N \--\> H;  
        M \-- Success/Fail \--\> J;  
    end

    A \--\> D;  
    B \--\> D;  
    C \--\> D;

---

## **Section 2: The Agentic Workforce: Roles, Responsibilities, and Technologies**

This section serves as the detailed specification for each component of the multi-agent system. It dissects the architecture into its constituent agents, defining the specific function, underlying technology, and contribution of each member of the agentic workforce. The following table provides a high-level summary for reference.

**Table 1: Agent Roles and Responsibilities**

| Agent Name | Core Responsibility | Key Technologies | Primary Output |
| :---- | :---- | :---- | :---- |
| **Ingestion Agent** | Monitors input channels (email, folders, API) and triggers new workflows. | IMAP Client, File System Watcher, REST API Framework (e.g., FastAPI). | Raw document file and initial metadata passed to the Orchestrator. |
| **Pre-processing & Classification Agent** | Enhances image quality and identifies the document type (e.g., invoice, packing list). | OpenCV, Donut (Document Understanding Transformer). | Cleaned document image and a classification label (e.g., doc\_type). |
| **Extraction Agent** | Extracts structured data from the document using a layout-aware model. | Layout-Aware LLM (e.g., DocLLM, GPT-4o), Vision-Language Models. | Structured data in a canonical JSON format. |
| **Validation Agent** | Programmatically verifies the accuracy and integrity of the extracted data. | Python, Regular Expressions, API Client for database lookups. | Enriched JSON with validation status and confidence scores for each field. |
| **Human-in-the-Loop (HITL) Agent** | Manages the workflow and UI for tasks requiring human review and correction. | Web Framework (e.g., React, Vue), Backend API for queue management. | Final, human-approved data passed to the Integration Agent. |
| **Integration Agent** | Formats the final data and executes API calls to update the target system. | Python, API Client, Data Transformation Libraries. | Final transaction status (success/failure) logged. |
| **Learning Agent** | Asynchronously collects corrections from the HITL process to create fine-tuning datasets. | Python, MLOps frameworks, Data storage (e.g., S3). | Periodically updated and improved versions of the extraction model. |

### **2.1 Ingestion Agent: The System's Front Door**

The Ingestion Agent acts as the primary entry point for all documents into the Project Digitize system. Its sole responsibility is to monitor all configured input channels, retrieve new documents as they arrive, and initiate a new workflow instance via the Orchestrator for each one. This agent must be robust and capable of handling various sources, a common requirement in enterprise IDP systems.3

The configured sources will include:

* **Email Inbox:** A dedicated email address (e.g., invoices@company.com) will be continuously monitored using an IMAP client. The agent will parse incoming emails, extract supported attachments (PDF, PNG, JPG, TIFF), and process them.  
* **Watched File System:** The agent will monitor a designated network folder or directory. When a new file is added to this directory (e.g., from a network scanner), the agent will pick it up for processing.  
* **API Endpoint:** A secure REST API endpoint will be exposed, allowing other internal or external systems to programmatically submit documents for processing. This provides a clean integration point for other applications.

Upon retrieving a document, the Ingestion Agent packages the raw file (e.g., invoice.pdf) along with initial metadata such as the source channel, timestamp, and original filename. It then makes a single call to the Orchestrator to start a new, uniquely identified workflow instance.

### **2.2 Pre-processing & Classification Agent: The Triage Specialist**

Once a workflow is initiated, the Orchestrator's first task is to invoke the Pre-processing & Classification Agent. This agent performs two critical functions that are essential for achieving high accuracy in the downstream extraction process.3

First, it performs **Image Pre-processing**. Scanned documents are often imperfect. They can be skewed, contain scanner noise, or have poor contrast. This agent applies a pipeline of standard computer vision techniques to clean and normalize the document image. This includes:

* **De-skewing:** Automatically detecting and correcting the rotation of a scanned page.  
* **Noise Reduction:** Applying filters to remove random speckles or "salt and pepper" noise.  
* **Binarization:** Converting the image to a high-contrast black and white format, which can improve character recognition.

Second, and most importantly, it performs **Document Classification**. The system needs to know what *kind* of document it is processing (e.g., "Samsung Commercial Invoice," "Janssen Sales Invoice," "Samsung Packing List") to apply the correct extraction logic and validation rules later on. For this task, a dedicated visual document classification model is the ideal tool. The recommended technology is a fine-tuned **Donut (Document Understanding Transformer)** model.12 Donut is an OCR-free model, meaning it learns to classify documents based on their overall visual layout and structure, rather than first reading the text.15 This makes it fast and highly effective for distinguishing between different templates. The agent would be trained on a labeled set of example documents and, during inference, would take the pre-processed image and return a classification label (e.g.,

doc\_type: "samsung\_invoice\_v1").

The agent's output—the cleaned document image and its classification label—is then passed back to the Orchestrator, which now has the necessary information to route the document to the appropriate extraction workflow.

### **2.3 The Extraction Agent: The Cognitive Core**

The Extraction Agent is the heart of the system, responsible for the most complex and mission-critical task: converting the unstructured visual document into a structured, machine-readable JSON object. The choice of technology for this agent has the most significant impact on the entire system's accuracy, flexibility, and cost.

#### **2.3.1 Technology Analysis: Why Layout-Aware LLMs are the Engine of Choice**

The primary challenge in this project is the variability of document layouts. A solution that works for the Samsung invoice 1 must also work for the Janssen invoice 1 without requiring manual reconfiguration. This rules out traditional, template-based OCR systems, which are brittle and require a new template for every layout variation.18 While standard LLMs can parse text, they are "blind" to the 2D spatial structure of a document and can easily get confused by tables, columns, and complex layouts.18

The state-of-the-art approach, and the one recommended for this system, is to use a **multimodal, layout-aware Large Language Model**. These models process both the visual information (the image) and the textual information simultaneously, allowing them to understand the crucial spatial relationships between data points on a page.

There are two primary categories of such models:

1. **Specialized Document AI Models:** Models like **DocLLM** 19 and  
   **LayoutLLM** 21 are specifically designed for this purpose. They are "light-weight" extensions to standard LLMs that incorporate the bounding box coordinates of text tokens directly into the model's attention mechanism. This allows the model to understand, for example, that a price in the fifth column belongs to the product description in the first column of the same row. This capability is essential for accurately parsing the line-item tables present in the sample documents.1  
2. **General-Purpose Vision-Language Models (VLMs):** Powerful, large-scale models like **GPT-4o** and **Google's Gemini** have demonstrated formidable capabilities in understanding and reasoning about visual inputs. They can effectively act as a one-step OCR and extraction engine, interpreting the document holistically.23 They are highly flexible and can often achieve strong results with zero-shot prompting, meaning they can handle new document layouts they have never seen before.26

The recommendation is to leverage one of these layout-aware approaches. This provides the necessary flexibility to handle the organization's current and future document diversity and the contextual understanding needed to correctly interpret complex structures like tables and forms.18

**Table 2: Technology Trade-off Analysis (Extraction Engine)**

| Feature | Template-Based OCR | OCR \+ Standard LLM | Layout-Aware LLM / VLM (Recommended) |
| :---- | :---- | :---- | :---- |
| **Accuracy (Variable Layouts)** | Low. Fails on unseen templates. | Medium. Can be confused by complex tables/columns. | High. Understands spatial context and generalizes well. |
| **Flexibility (New Docs)** | Very Low. Requires manual template creation for each new format. | Medium. LLM can adapt, but OCR may still need tuning. | High. Can often handle new formats with zero-shot prompting. |
| **Development Effort** | High. Significant upfront and ongoing effort to create and maintain templates. | Medium. Requires integrating two separate systems (OCR and LLM). | Low to Medium. Primarily involves prompt engineering and API integration. |
| **Cost (Per Document)** | Low. Once licensed, per-page costs are minimal. | High. Combines costs of both OCR and LLM token usage. | Medium/Variable. Usage-based pricing scales with volume and complexity.18 |
| **Latency** | Low. Very fast, often milliseconds per page.18 | High. Sum of latencies from both OCR and LLM calls. | Medium. Slower than OCR but faster than a two-step process.18 |
| **Recommendation** | Not suitable for this project due to lack of flexibility. | A viable but suboptimal and complex approach. | **Recommended.** Offers the best balance of accuracy, flexibility, and manageable development effort for handling diverse document formats. |

#### **2.3.2 Dynamic Field Mapping and Named Entity Recognition (NER)**

The Extraction Agent will leverage the LLM's powerful Natural Language Processing capabilities to perform dynamic field mapping using a technique similar to zero-shot Named Entity Recognition (NER).26 Instead of being programmed with rigid rules about where to find data, the agent is given a target schema in its prompt.

Based on the classification label received from the Orchestrator (e.g., "janssen\_invoice\_v2"), the Orchestrator selects a predefined JSON schema and includes it in the prompt to the Extraction Agent. For example, for the Janssen invoice 1, the prompt would look like this:

Given the following document image, extract the relevant information and return it as a valid JSON object matching this schema. Do not invent information. If a field is not present, use null. Schema: { "invoice\_number": "...", "invoice\_date": "...", "payer\_name": "...", "line\_items": \[ { "product\_description": "...", "tariff\_number": "...", "batch\_number": "...", "expiry\_date": "...", "quantity": 0, "unit\_price": 0.0, "total\_value": 0.0 } \], "grand\_total": 0.0 }

The layout-aware LLM uses its understanding of language ("Payer," "Date," "Quantity") and layout (the tabular structure of the line items) to accurately populate this JSON object. This prompt-driven approach is vastly more flexible and resilient to layout changes than hard-coded extraction logic.18

### **2.4 Validation Agent: The Quality Assurance Inspector**

An LLM's output, while powerful, is not infallible and can sometimes "hallucinate" or make subtle errors.25 The Validation Agent serves as an essential, programmatic quality assurance gate. Its responsibility is to verify the accuracy and integrity of the data extracted by the LLM before it is sent to a human or the final system. This agent applies a cascade of automated checks 4:

1. **Format Validation:** It ensures that the extracted data conforms to expected formats. For example, it verifies that date fields are valid dates, numeric fields contain only numbers, and that specific fields like the G.T.İ.P. code match a predefined regular expression (e.g., \\d{4}.\\d{2}.\\d{4}.\\d{2}.\\d{2}).  
2. **Business Rule Validation:** It applies mathematical and logical checks based on rules specific to the document type. For the Janssen invoice 1, it would verify that the line item calculation is correct (  
   4,000×55.36=221,440.00). For the Samsung invoice 1, it would sum all the "Amount" column values and check if they equal the "TOTAL" value.  
3. **Cross-Reference Validation:** This is a crucial step where the agent interacts with existing systems via their APIs. It can take an extracted Payer ID (e.g., 0000024048 from 1) or  
   PO no. (e.g., 3074720026 from 1) and query the existing database to confirm that the customer or purchase order is valid and exists.

After performing these checks, the agent generates a confidence score for each extracted field. A field that passes all checks retains a high score (e.g., 99%). A field that fails a validation (e.g., a total that doesn't add up) will have its confidence score significantly penalized. The final output is an enriched JSON object containing the data, a detailed validation report, and a confidence score for every field.

### **2.5 Human-in-the-Loop (HITL) Agent: The Human Supervisor**

The HITL Agent is responsible for managing the workflow and interface for all documents that require human judgment. This is not merely an error-handling mechanism but a core design principle of the system, ensuring the highest levels of accuracy for critical data and providing the feedback necessary for continuous improvement.6

When the Orchestrator receives a validation result from the Validation Agent with low-confidence scores or failed business rules, it does not proceed automatically. Instead, it routes the task to the HITL Agent. This agent's function is to manage a work queue for human reviewers. It assigns the flagged document to an available operator, presents a specialized review interface (detailed in Section 4), captures the human's corrections or approval, and then passes the finalized, 100% correct data back to the Orchestrator to continue the workflow. This ensures that the speed of automation is balanced with the precision and contextual understanding that only a human can provide in ambiguous cases.33

### **2.6 Integration Agent: The Final Mile**

The Integration Agent is responsible for the final step of the workflow: successfully posting the validated and approved data to the target system. Its tasks are precise and critical for completing the process.

First, it performs **Data Transformation**. The canonical JSON format used internally by the agentic system may not match the exact payload structure required by the target system's APIs. This agent transforms the data, mapping field names (e.g., header.invoiceId to ref\_no), reformatting values (e.g., date formats), and constructing the final request body.

Second, it handles **API Interaction**. The agent executes the necessary API calls (e.g., a POST request to /api/v1/invoices) to create or update records in the existing database.

Finally, it manages **Error Handling** at the integration layer. It is responsible for handling API-level errors such as network timeouts, authentication failures, or business logic rejections from the target system (e.g., "Duplicate Invoice Number"). It will employ a defined retry policy for transient errors and will flag persistent, unresolvable errors for manual investigation by an administrator. Upon completion, it logs the final transaction status (success or failure) and reports back to the Orchestrator.

### **2.7 Learning Agent: The System's Brain Trainer**

The Learning Agent is the component that enables the system to evolve and become more intelligent over time. It embodies the principle of continual learning, ensuring that the system's accuracy is not static but improves with use.36 This agent operates asynchronously in the background and is not part of the real-time document processing pipeline.

Its workflow is driven by feedback from the HITL process:

1. **Collects Correction Data:** The agent subscribes to "correction events" published by the HITL Agent. Whenever a human reviewer corrects a field, the Learning Agent receives a data packet containing the document image, the LLM's original incorrect prediction, and the human's verified correct label.  
2. **Builds Fine-Tuning Datasets:** It aggregates these correction pairs over time, building a high-quality, structured dataset that is perfectly suited for fine-tuning the core extraction model.  
3. **Triggers and Manages Retraining:** On a scheduled basis (e.g., weekly) or after a certain threshold of new correction samples has been collected, the agent automatically initiates a fine-tuning job for the Extraction Agent's LLM.  
4. **Manages Model Versioning:** It tracks different versions of the fine-tuned models, evaluates their performance against a held-out "golden" dataset, and manages their deployment. This allows for safe updates and rollbacks if a newly trained model shows any signs of regression.

The agentic architecture provides a distinct advantage here. Because the Learning Agent is a completely separate, decoupled component, its resource-intensive work of data aggregation and model training has zero impact on the performance or stability of the live, real-time processing pipeline. This architectural separation makes implementing a robust, safe, and efficient continual learning cycle significantly more practical and is a direct benefit of adopting the MAS paradigm from the outset.

---

## **Section 3: The Document Processing Pipeline in Detail**

This section provides a granular, step-by-step narrative of a single document's journey through the Project Digitize system. It illustrates the concrete interactions between the Orchestrator and the subordinate agents, making the abstract architectural concepts tangible. The sequence diagram below focuses on the critical extraction stage.

### **3.1 Stage 1: Document Ingestion and Triage**

The process begins when a new document, for instance, the Janssen sales invoice 1, arrives as a PDF attachment in the designated email inbox. The

**Ingestion Agent**, which is constantly monitoring this inbox, detects the new email, downloads the PDF attachment, and extracts initial metadata (e.g., source: "email", received\_at: "timestamp"). The agent then makes a single API call to the **Orchestrator** to initiate a new workflow, passing along the PDF file and its metadata. The Orchestrator logs the start of the process, assigns it a unique workflow tracking ID (e.g., wf-a1b2c3d4), and persists its initial state.

### **3.2 Stage 2: Intelligent Classification and Routing**

The Orchestrator's first action is to invoke the **Pre-processing & Classification Agent**. The agent receives the PDF, converts the first page to a high-resolution image, and applies its pre-processing pipeline (de-skewing, noise reduction). The cleaned image is then passed to its internal, fine-tuned Donut classification model.15 The model analyzes the visual layout—the position of the Janssen logo, the structure of the address blocks, the single large table—and returns a classification result:

{"class": "janssen\_invoice\_v2"}. The agent reports this classification label back to the Orchestrator, which updates the workflow's state.

### **3.3 Stage 3: Contextual Data Extraction**

Now equipped with the document's type, the Orchestrator can proceed with extraction. It retrieves the predefined JSON schema prompt specifically designed for a "janssen\_invoice\_v2". It then invokes the **Extraction Agent**, passing it the cleaned document image and this contextual schema prompt. The Extraction Agent's internal layout-aware LLM 20 gets to work. It analyzes the document holistically, using both the text content and the spatial layout to fulfill the prompt's request. It correctly identifies "2100504266" as the "Number," associates "ТОРАМАХ 100MG 60 TABL. TURK." with the product information, and correctly extracts the quantity, unit price, and value from the table. The agent then returns the fully populated, structured JSON object to the Orchestrator.

Kod snippet'i

sequenceDiagram  
    participant O as Orchestrator  
    participant E as Extraction Agent  
    participant LLM as Layout-Aware LLM

    O-\>\>E: ExecuteExtraction(image, schema\_prompt\_for\_janssen\_v2)  
    Note over O,E: Orchestrator provides context via the prompt.  
    E-\>\>LLM: ProcessDocument(image, schema\_prompt)  
    Note over LLM: Model analyzes both visual layout and text content to map fields. It understands the table structure.  
    LLM--\>\>E: Return structured\_JSON  
    E--\>\>O: Return ExtractionResult(structured\_JSON)

### **3.4 Stage 4: Automated and Rule-Based Validation**

The Orchestrator receives the extracted JSON and immediately invokes the **Validation Agent**. The agent begins its cascade of checks:

1. **Format Check:** It confirms the invoice\_date is a valid date and all monetary fields are valid numbers. It checks that the TARIFF NUMBER (3004.9000.000 from 1) matches the expected RegEx pattern.  
2. **Business Rule Check:** It performs the calculation: quantity 4,000 multiplied by unit price 55.36 equals 221,440.00. It confirms this matches the extracted Value in TRY.  
3. **Cross-Reference Check:** It takes the Payer ID (0000024048) and makes an API call to the existing company database (GET /api/v1/customers?id=0000024048). The API returns a success response, confirming the payer is a valid entity.

Since all checks pass, the agent returns the JSON to the Orchestrator with a validation\_status: "success" and high confidence scores (e.g., \>98%) for all fields.

### **3.5 Stage 5: Human Review and Correction (The HITL Workflow)**

In this instance, since all validations passed with high confidence, the system's confidence gate allows the document to proceed directly to the next stage, achieving Straight-Through Processing (STP).

However, let's consider an alternative scenario where the scanner quality was poor and the LLM misread the quantity as "4,00S". In this case, the Validation Agent's format check would fail for the quantity field, and the business rule calculation would also fail. The agent would return a low confidence score for the quantity and total value fields. The Orchestrator's confidence gate would detect this low score and automatically route the workflow to the **HITL Agent**.

The HITL agent would place the document in a human reviewer's work queue. The reviewer would open the UI, see the quantity field highlighted in red with a "Format Error" warning. They would examine the document image, correct the "4,00S" to "4,000" in the form, and click "Approve." The HITL agent would then pass the corrected, fully approved data back to the Orchestrator. In parallel, it would send the correction data— (image, field: 'quantity', original: '4,00S', corrected: '4000') —to the **Learning Agent** for future model improvement.

### **3.6 Stage 6: Finalization and System Integration**

The Orchestrator now possesses a fully validated and correct data payload (either directly from the Validation Agent or after HITL correction). It invokes the **Integration Agent**. This agent takes the canonical JSON, transforms it into the specific format required by the target system's API (as seen in the screenshot, with fields like Mal Cinsi, Miktar, Fatura Tutarı), and executes the final POST request to the API endpoint. The target system's API processes the request and returns a 200 OK success status. The Integration Agent reports this success back to the Orchestrator, which marks the entire workflow instance as complete and logs the successful outcome.

---

## **Section 4: The Human-in-the-Loop Subsystem: The Cornerstone of Accuracy**

The Human-in-the-Loop (HITL) subsystem is not an afterthought or a simple error queue; it is a foundational component of the architecture designed to guarantee data quality, handle ambiguity, and drive continuous improvement. By intelligently combining the speed of automation with the nuanced judgment of human experts, the HITL subsystem ensures that Project Digitize is both efficient and trustworthy.6

### **4.1 The HITL Activation Protocol**

The decision to engage a human reviewer is governed by a clear, configurable, and automated protocol. A document is routed to the HITL queue if and only if one of the following conditions is met, ensuring that human attention is focused exclusively where it adds the most value 6:

* **Low Confidence Score:** Any individual field with a confidence score falling below a predefined and configurable threshold (e.g., a threshold of 95%) will trigger a review. This is the primary mechanism for catching potential LLM misinterpretations or OCR-like errors.  
* **Failed Business Rule:** Any hard failure reported by the Validation Agent, such as a line-item sum not matching the grand total or a tax calculation being incorrect, will automatically require human sign-off.  
* **Missing Critical Fields:** If the Extraction Agent fails to find a field designated as mandatory in the document schema (e.g., Invoice Number, Grand Total, Supplier Name), the document cannot be processed automatically and must be reviewed.  
* **New Document Type Encountered:** When the Classification Agent identifies a document layout for the first time (e.g., a new supplier sends their first invoice), the system can be configured to automatically route the first 'N' (e.g., 5\) instances of this new type for human verification. This helps build a trusted baseline for the new format and ensures the extraction schema is working correctly before allowing STP.

### **4.2 Blueprint for the Review Interface**

The efficiency and accuracy of the human review process are critically dependent on the design of the review interface. A poorly designed UI can lead to fatigue, errors, and slow processing. The proposed interface is based on established best practices for HITL systems 33 and is designed to be transparent, efficient, and context-rich.

The interface will be a single-page web application with three main panels:

1. **Document Viewer Panel (Left):** This panel will display a high-fidelity, interactive rendering of the original document image. Users will be able to pan, zoom, and rotate the document to inspect details clearly.  
2. **Extracted Data Form Panel (Right):** This panel will contain a web form with fields corresponding to the canonical data schema. Each field will display the data extracted by the AI.  
3. **Validation & Audit Panel (Bottom Right):** This panel will provide metadata about the review task, including any specific validation warnings (e.g., "Warning: Sum of line items does not match total.") and an audit trail of changes.

**Key Interactive Features:**

* **Synchronized Highlighting:** When a user clicks on a form field in the right panel (e.g., "Invoice Date"), the corresponding text in the document image on the left panel will be instantly highlighted with its detected bounding box. This immediately provides visual context and allows the reviewer to verify the source of the data without searching.  
* **Visual Confidence Indicators:** Each form field will have a visual indicator of its AI-generated confidence score. For example, a green border for scores \>95%, a yellow border for scores between 80-95%, and a red border for scores \<80% or for fields that failed a validation rule. This immediately draws the reviewer's attention to the most likely problem areas.  
* **Efficient Correction:** Reviewers can directly type into the form fields to make corrections. The interface will support keyboard shortcuts (e.g., Tab to move to the next field, Enter to approve) to maximize throughput.  
* **Action Buttons:** Clear and concise action buttons ("Approve", "Save & Next", "Flag for Escalation") will allow the reviewer to finalize their work or send a particularly problematic document to a senior administrator.

### **4.3 The Feedback Loop: Fueling Continuous Improvement**

The HITL subsystem is the primary engine for the system's long-term learning. Every correction made by a human reviewer is a valuable piece of training data that can be used to make the AI model smarter.6 This is managed through a non-blocking feedback loop.

When a reviewer corrects a value in the UI and clicks "Approve," two actions occur in parallel:

1. The approved, correct data is sent back to the Orchestrator to continue the main processing workflow.  
2. A structured feedback event is generated and published to a dedicated message queue.

This feedback event is a self-contained JSON object that captures the complete context of the correction:

JSON

{  
  "document\_id": "wf-a1b2c3d4",  
  "document\_class": "janssen\_invoice\_v2",  
  "field\_name": "quantity",  
  "original\_extraction": "4,00S",  
  "corrected\_value": "4000",  
  "confidence\_before\_correction": 0.45,  
  "bounding\_box\_coordinates": \[x1, y1, x2, y2\],  
  "reviewer\_id": "operator\_1138",  
  "timestamp": "2024-10-26T14:30:00Z"  
}

This event-driven approach ensures that the feedback capture process is completely decoupled from the main workflow, imposing no additional latency on the reviewer. The **Learning Agent** subscribes to this queue, asynchronously consuming these events to build the datasets needed for model fine-tuning, thus completing the continual learning cycle.

**Table 4: Human-in-the-Loop (HITL) Performance KPIs**

To ensure the HITL subsystem is operating efficiently and effectively, its performance will be tracked using a set of key performance indicators (KPIs). This data is essential for identifying bottlenecks, measuring the impact of model improvements, and managing operational costs.

| KPI Name | Description | Formula / Method | Business Goal |
| :---- | :---- | :---- | :---- |
| **Straight-Through Processing (STP) Rate** | The percentage of documents processed automatically with no human intervention. | (Total Docs \- Docs Sent to HITL) / Total Docs | Maximize this rate to reduce manual effort and operational cost. This is the primary measure of overall automation success. |
| **Override Rate (per field)** | The percentage of time a specific extracted field is corrected by a human. | (Corrections for Field X) / (Times Field X was Reviewed) | Minimize this rate. High rates for specific fields indicate areas where the extraction model is struggling and needs improvement. |
| **Average Review Time per Document** | The average time a human reviewer spends on a single document in the HITL interface. | Total Review Time / Number of Reviewed Docs | Minimize this time to improve reviewer productivity. Spikes may indicate UI issues or particularly difficult document batches. |
| **Post-Review Accuracy** | The accuracy of data after it has been through the HITL process, measured by periodic quality audits. | (1 \- (Errors Found in Audit / Audited Docs)) \* 100 | Target 99.9% or higher. This measures the effectiveness of the human review process itself. |

---

## **Section 5: Data Modeling and Integration Strategy**

This section defines the critical interface between the Project Digitize system and the organization's existing technical landscape. A clear and robust data and integration strategy is essential for ensuring that the high-quality data produced by the agents can be consumed reliably by downstream systems.

### **5.1 The Canonical Data Schema**

To handle the diversity of input documents, the system will define and use a single, standardized internal data structure known as the **Canonical Data Schema**. This schema acts as a universal language or a "Rosetta Stone" for the system. Regardless of whether the input is a Samsung invoice or a Janssen packing list, the Extraction Agent's output will always conform to this single, predictable JSON structure. This approach dramatically simplifies all downstream processing, including validation, human review, and final integration, as these components only ever need to be programmed to handle one consistent data format.

The schema will be designed as a superset of all required fields identified from the provided sample documents (1) and the target system's user interface.

**Table 3: Canonical Data Output Schema (Partial Example)**

| Canonical Field Path | Data Type | Description | Source Document Mapping Example | Target System Mapping |
| :---- | :---- | :---- | :---- | :---- |
| header.documentId | String | The primary identifier of the document. | Samsung: "Invoice No.", Janssen: "Number" | Ref. No: |
| header.documentType | String | The type of the document as determined by the Classification Agent. | N/A | (Used for internal routing) |
| header.issueDate | String (ISO 8601\) | The date the document was issued. | Samsung: "Date", Janssen: "Date" | (Implicit in Tarih) |
| header.currency | String (ISO 4217\) | The currency code for monetary values. | Detected from document (e.g., "USD", "TRY"). | Döviz Kuru |
| seller.name | String | The name of the selling party. | Samsung: "Seller", Janssen: "Payer" (in context) | Firma |
| buyer.name | String | The name of the buying party. | Samsung: "Buyer", Janssen: "Consignee" | (Implicit in company context) |
| lineItems | Array\[Object\] | An array containing each line item from the document. | Table rows in all documents. | The main item grid. |
| lineItems.description | String | The description of the product or service. | Samsung: "Goods description", Janssen: "Product information" | Mal Cinsi |
| lineItems.gtipCode | String | The Harmonized System tariff code. | Janssen: "TARIFF NUMBER" | G.T.İ.P. |
| lineItems.quantity | Number | The quantity of the item. | Samsung: "Quantity", Janssen: "Quantity UOM" | Miktar |
| lineItems.unitPrice | Number | The price per unit of the item. | Samsung: "Unit price", Janssen: "Unit price in TRY" | (Used to calculate Fatura Bedeli) |
| summary.netTotal | Number | The total value before taxes or other charges. | Samsung: (Calculated), Janssen: (Implicit) | Net |
| summary.grossTotal | Number | The final, total amount of the invoice. | Samsung: "Amount" (Total), Janssen: "Value in TRY" (Total) | Fatura Bedeli |

### **5.2 API Interaction Protocol and Contract**

The system is designed to integrate with an existing set of APIs for both retrieving validation data and submitting the final, processed data. This section outlines the expected interaction patterns.

For the Validation Agent:  
The Validation Agent will primarily use GET requests to fetch data for cross-referencing. The API contracts are expected to be stable and well-documented.

* **Example Lookup:** To verify a purchase order.  
  * **Method:** GET  
  * **Endpoint:** /api/v1/purchase\_orders/{po\_number}  
  * **Example Call:** GET /api/v1/purchase\_orders/3074720026  
  * **Expected Success Response (200 OK):** A JSON object containing PO details, which can be used to verify supplier and item details.  
  * **Expected Failure Response (404 Not Found):** Indicates the PO does not exist, which would cause the validation to fail.

For the Integration Agent:  
The Integration Agent will use POST or PUT requests to submit the final, structured data to the target system.

* **Example Submission:** To create a new invoice record in the target system.  
  * **Method:** POST  
  * **Endpoint:** /api/v1/declarations  
  * **Request Body:** A JSON payload constructed from the canonical schema, transformed to match the specific requirements of this endpoint.  
  * **Expected Success Response (201 Created):** A JSON response including the ID of the newly created record.  
  * **Expected Failure Response (400 Bad Request / 409 Conflict):** A JSON response with an error message, such as "Invalid customer ID" or "Invoice number already exists." The Integration Agent must be ableto parse these errors and flag the workflow for manual review.

### **5.3 Strategy for Handling Database Variations and Lookups**

A common challenge in data integration is mapping varied textual information from source documents to a single, unique key in a database. For instance, a supplier might be listed as "PT SAMSUNG ELECTRONICS INDONESIA" on one document 1 and simply "SAMSUNG" in another context. The system cannot rely on an exact string match for lookups.

To solve this, the proposed strategy is to implement an **Entity Alias Service**. This service would maintain a dedicated table or collection in the database that maps various known aliases to a single, canonical entity ID.

* **Example Alias Table Entry:**  
  * canonical\_id: CUST-0048  
  * canonical\_name: "Johnson & Johnson SIHHI MALZEME SAN.VE TIC.LTD.STI."  
  * aliases: \`\`

When the Validation Agent extracts a supplier name like "JOHNSON2" (from the UI screenshot), it will not query the main customer table directly. Instead, it will query the Entity Alias Service. The service will find the matching alias and return the canonical ID (CUST-0048), which can then be used for reliable lookups and data linkage in the target system. This layer of abstraction makes the validation process significantly more robust and resilient to variations in source data.

---

## **Section 6: System Evolution: Scalability, Reliability, and Learning**

This final section outlines the strategic vision for the long-term operation and evolution of Project Digitize. The architecture is designed not as a static, one-time solution, but as a dynamic platform that can grow with the business, maintain high levels of reliability, and continuously improve its own intelligence.

### **6.1 Architectural Provisions for Scalability**

The decoupled, agent-based architecture is the cornerstone of the system's scalability.7 Unlike a monolithic application that scales as a single unit, the MAS allows for targeted, efficient scaling of individual components.

* **Component-wise Scaling:** Each agent will be packaged as a lightweight, containerized service (e.g., using Docker). These containers can be deployed and managed by an orchestration platform like Kubernetes. This platform can be configured to monitor the task queue for each agent type and automatically scale the number of running containers based on demand. For example, if a large batch of 10,000 documents is submitted, the Orchestrator will create 10,000 tasks for the Extraction Agent. Kubernetes can be configured to detect this surge in the extraction queue and automatically spin up additional Extraction Agent containers to process the workload in parallel. Once the queue subsides, it will scale them back down, ensuring efficient use of computing resources.  
* **Asynchronous Processing:** The use of an orchestration engine like Temporal and message queues for inter-agent communication means the entire system is asynchronous. This prevents any single slow agent from blocking the entire pipeline and allows the system to gracefully handle back-pressure and variable processing times.  
* **Database and API Scalability:** It is critical to note that the overall system's throughput will ultimately be limited by the performance of the external systems it integrates with, namely the existing database and APIs. As part of the implementation phase, load testing must be conducted to identify and address any potential bottlenecks in these downstream dependencies to ensure they can handle the increased transaction volume from the automated system.

### **6.2 The Continual Learning Cycle**

The system is designed to become more accurate and efficient over time through a robust, automated continual learning cycle. This MLOps (Machine Learning Operations) process ensures that the intelligence of the core Extraction Agent evolves, adapting to new document formats and correcting its own past mistakes without requiring manual intervention from developers.37

The full end-to-end cycle is as follows:

1. **Feedback Capture:** The HITL subsystem automatically captures every human correction as a structured data point, as detailed in Section 4.3.  
2. **Dataset Aggregation:** The background **Learning Agent** consumes these correction events and aggregates them into a high-quality, versioned fine-tuning dataset.  
3. **Scheduled Fine-Tuning:** On a regular schedule (e.g., weekly), an automated job is triggered to fine-tune a new version of the Extraction Agent's LLM using the latest aggregated dataset.  
4. **Mitigating Catastrophic Forgetting:** A critical challenge in continual learning is ensuring that when a model learns a new task, it doesn't forget how to perform older ones.36 To prevent this, the fine-tuning process will use a technique called  
   **experience replay**. The training data will consist not only of the new correction samples but also a representative sample of data from all previously seen document types. This reminds the model of past knowledge while it incorporates new information.37  
5. **Automated Evaluation:** After fine-tuning, the new model version is automatically evaluated against a "golden", held-out test set that contains a diverse mix of challenging documents. Its performance (accuracy, precision, recall) is compared against the currently deployed production model.  
6. **Champion/Challenger Deployment:** If the new "challenger" model outperforms the current "champion" model, it is promoted and deployed into production. This can be done with zero downtime. If it does not, the current model remains in place, and the results are flagged for review by the AI team.  
7. **Monitoring:** The performance of the live model is continuously monitored to detect any concept drift or degradation in accuracy, which would trigger an alert and potentially a new training cycle.

### **6.3 Framework for System Monitoring and Observability**

A complex, distributed system like Project Digitize requires comprehensive monitoring to ensure reliability, diagnose issues, and track performance. A centralized observability platform (such as Splunk, Datadog, or an open-source stack like Prometheus, Grafana, and Loki) will be used to aggregate logs, metrics, and traces from all agents and the orchestrator.

The following key metrics will be tracked on dashboards:

* **Business Metrics:**  
  * Documents Processed per Hour/Day  
  * Average End-to-End Processing Time (from ingestion to integration)  
  * Straight-Through Processing (STP) Rate  
  * Total Cost per Document Processed  
* **Agent Performance Metrics:**  
  * Task Queue Length for each agent type  
  * Average Task Latency (processing time) for each agent  
  * Error Rate and Retry Count for each agent  
* **AI Model Metrics:**  
  * Distribution of Confidence Scores from the Validation Agent  
  * Field-Specific Accuracy and Override Rates from the HITL system  
  * Classification Accuracy of the Classification Agent  
* **System Health Metrics:**  
  * CPU and Memory Utilization of agent containers  
  * Latency and Error Rates of API calls to external systems  
  * Database connection pool usage

These dashboards will provide a real-time, holistic view of the system's health and performance, enabling proactive issue resolution and data-driven decision-making for future optimizations.

---

## **Appendix: Recommended Technology Stack**

This section provides a summary of concrete technology recommendations to serve as a starting point for implementation planning and proof-of-concept development.

* **Orchestration Engine:**  
  * **Temporal.io:** Recommended for its durability, scalability, and built-in support for managing complex, stateful, and asynchronous workflows.  
* **Agent Framework & Services:**  
  * **Python:** The primary language for developing the agents due to its rich ecosystem of AI/ML libraries.  
  * **Containerization:** Docker for packaging agents and Kubernetes for deployment, scaling, and management.  
  * **Agent Development:** LangChain or LlamaIndex can be used to accelerate the development of LLM-powered agents, or agents can be built as custom Python services using a web framework like FastAPI.  
* **AI & Machine Learning Models:**  
  * **Cloud Services (Managed Option):**  
    * **AWS:** Amazon Textract (for pre-processing/layout analysis), Amazon Bedrock (to access and fine-tune a variety of foundation models like Claude 3), Amazon SageMaker (for custom model training and hosting).  
    * **Google Cloud:** Document AI Platform (for specialized processors), Vertex AI (for Gemini models and model training).  
  * **Self-Hosted/Fine-tuned (Flexible Option):**  
    * **Extraction LLM:** A powerful open-source model like Llama 3 or a specialized layout-aware model like **DocLLM**.  
    * **Classification Model:** A fine-tuned **Donut** model.  
* **Infrastructure & Data Stores:**  
  * **Cloud Provider:** AWS, Google Cloud, or Azure.  
  * **Object Storage:** Amazon S3 or Google Cloud Storage for storing documents and model artifacts.  
  * **Message Queues:** Amazon SQS or RabbitMQ for asynchronous communication between agents (e.g., HITL feedback loop).  
* **Monitoring & Observability:**  
  * **Commercial:** Datadog, Splunk.  
  * **Open Source:** Prometheus (for metrics), Grafana (for dashboards), and Loki (for logs).  
* **API Management:**  
  * **API Gateway:** A dedicated gateway (e.g., Amazon API Gateway, Kong) to secure, rate-limit, and manage the public-facing Ingestion API endpoint.

#### **Alıntılanan çalışmalar**

1. 2640316788\_Packing List\_1.pdf  
2. What Is Intelligent Document Processing (IDP)? | Microsoft Power Automate, erişim tarihi Temmuz 20, 2025, [https://www.microsoft.com/en-us/power-platform/products/power-automate/topics/business-process/intelligent-document-processing](https://www.microsoft.com/en-us/power-platform/products/power-automate/topics/business-process/intelligent-document-processing)  
3. Understanding Intelligent Document Processing Workflow: Benefits ..., erişim tarihi Temmuz 20, 2025, [https://www.docsumo.com/blog/intelligent-document-processing-workflow](https://www.docsumo.com/blog/intelligent-document-processing-workflow)  
4. What is Intelligent Document Processing (IDP)? \- Automation Anywhere, erişim tarihi Temmuz 20, 2025, [https://www.automationanywhere.com/rpa/intelligent-document-processing](https://www.automationanywhere.com/rpa/intelligent-document-processing)  
5. What is Intelligent Document Processing? \- IDP Explained \- AWS, erişim tarihi Temmuz 20, 2025, [https://aws.amazon.com/what-is/intelligent-document-processing/](https://aws.amazon.com/what-is/intelligent-document-processing/)  
6. Human In The Loop (HITL) for AI Document Processing → Unstract.com, erişim tarihi Temmuz 20, 2025, [https://unstract.com/blog/human-in-the-loop-hitl-for-ai-document-processing/](https://unstract.com/blog/human-in-the-loop-hitl-for-ai-document-processing/)  
7. Understanding Agents and Multi Agent Systems for Better AI ..., erişim tarihi Temmuz 20, 2025, [https://hatchworks.com/blog/ai-agents/multi-agent-systems/](https://hatchworks.com/blog/ai-agents/multi-agent-systems/)  
8. 5 Tips for Creating a Scalable Documentation System \- BetterDocs, erişim tarihi Temmuz 20, 2025, [https://betterdocs.co/tips-to-create-scalable-documentation-system/](https://betterdocs.co/tips-to-create-scalable-documentation-system/)  
9. Multi-Agent Workflows: Use Cases & Architecture with Temporal, erişim tarihi Temmuz 20, 2025, [https://temporal.io/blog/what-are-multi-agent-workflows](https://temporal.io/blog/what-are-multi-agent-workflows)  
10. Building Multi-Agent Workflows with n8n, AutoGen and Mindpal: A Direct Guide \- Reddit, erişim tarihi Temmuz 20, 2025, [https://www.reddit.com/r/n8n/comments/1i12ja8/building\_multiagent\_workflows\_with\_n8n\_autogen/](https://www.reddit.com/r/n8n/comments/1i12ja8/building_multiagent_workflows_with_n8n_autogen/)  
11. Scalable Intelligent Document Processing with Textract, OpenSearch, and Bedrock \-, erişim tarihi Temmuz 20, 2025, [https://invisibl.io/blog/scalable-intelligent-document-processing-with-textract-opensearch-and-bedrock/](https://invisibl.io/blog/scalable-intelligent-document-processing-with-textract-opensearch-and-bedrock/)  
12. Donut \- Hugging Face, erişim tarihi Temmuz 20, 2025, [https://huggingface.co/docs/transformers/model\_doc/donut](https://huggingface.co/docs/transformers/model_doc/donut)  
13. Document AI: Fine-tuning Donut for document-parsing using Hugging Face Transformers, erişim tarihi Temmuz 20, 2025, [https://www.philschmid.de/fine-tuning-donut](https://www.philschmid.de/fine-tuning-donut)  
14. End-End model for Visual Document Understanding : Donut | by Sreenila Rajesh | Medium, erişim tarihi Temmuz 20, 2025, [https://medium.com/@sreenilarajesh/end-end-model-for-visual-document-understanding-donut-ef7d35eef63d](https://medium.com/@sreenilarajesh/end-end-model-for-visual-document-understanding-donut-ef7d35eef63d)  
15. Donut: Document Understanding Transformer \- Kaggle, erişim tarihi Temmuz 20, 2025, [https://www.kaggle.com/code/yesdeepakmittal/donut-document-understanding-transformer](https://www.kaggle.com/code/yesdeepakmittal/donut-document-understanding-transformer)  
16. How to use Donut, the document understanding Transformer for document Classification, Parsing and document Question and Answering\! | by Renix Informatics | Medium, erişim tarihi Temmuz 20, 2025, [https://medium.com/@renix\_informatics/how-to-use-donut-the-document-understanding-transformer-for-document-classification-parsing-and-fde0c7efa3f3](https://medium.com/@renix_informatics/how-to-use-donut-the-document-understanding-transformer-for-document-classification-parsing-and-fde0c7efa3f3)  
17. clovaai/donut: Official Implementation of OCR-free Document Understanding Transformer (Donut) and Synthetic Document Generator (SynthDoG), ECCV 2022 \- GitHub, erişim tarihi Temmuz 20, 2025, [https://github.com/clovaai/donut](https://github.com/clovaai/donut)  
18. Document Data Extraction in 2025: LLMs vs OCRs \- Vellum AI, erişim tarihi Temmuz 20, 2025, [https://www.vellum.ai/blog/document-data-extraction-in-2025-llms-vs-ocrs](https://www.vellum.ai/blog/document-data-extraction-in-2025-llms-vs-ocrs)  
19. Paper Review: DocLLM: A layout-aware generative language model for multimodal document understanding \- Andrew Lukyanenko, erişim tarihi Temmuz 20, 2025, [https://artgor.medium.com/paper-review-docllm-a-layout-aware-generative-language-model-for-multimodal-document-06b5833e976b](https://artgor.medium.com/paper-review-docllm-a-layout-aware-generative-language-model-for-multimodal-document-06b5833e976b)  
20. DocLLM: A layout-aware generative language model for multimodal document understanding \- arXiv, erişim tarihi Temmuz 20, 2025, [https://arxiv.org/html/2401.00908v1](https://arxiv.org/html/2401.00908v1)  
21. LayoutLLM: Layout Instruction Tuning with Large Language Models for Document Understanding \- CVF Open Access, erişim tarihi Temmuz 20, 2025, [https://openaccess.thecvf.com/content/CVPR2024/papers/Luo\_LayoutLLM\_Layout\_Instruction\_Tuning\_with\_Large\_Language\_Models\_for\_Document\_CVPR\_2024\_paper.pdf](https://openaccess.thecvf.com/content/CVPR2024/papers/Luo_LayoutLLM_Layout_Instruction_Tuning_with_Large_Language_Models_for_Document_CVPR_2024_paper.pdf)  
22. \[2403.14252\] LayoutLLM: Large Language Model Instruction Tuning for Visually Rich Document Understanding \- arXiv, erişim tarihi Temmuz 20, 2025, [https://arxiv.org/abs/2403.14252](https://arxiv.org/abs/2403.14252)  
23. What is OCR Data Extraction? \- Roboflow Blog, erişim tarihi Temmuz 20, 2025, [https://blog.roboflow.com/ocr-data-extraction/](https://blog.roboflow.com/ocr-data-extraction/)  
24. OCR vs LLMs: What's the Best Tool for Document Processing? \- TableFlow, erişim tarihi Temmuz 20, 2025, [https://tableflow.com/blog/ocr-vs-llms](https://tableflow.com/blog/ocr-vs-llms)  
25. Using LLMs for document OCR: What you need to know | Apr 09, 2025 \- Cradl AI, erişim tarihi Temmuz 20, 2025, [https://www.cradl.ai/post/llm-ocr](https://www.cradl.ai/post/llm-ocr)  
26. GVDIE: A Zero-Shot Generative Information Extraction Method for Visual Documents Based on Large Language Models \- APSIPA ASC 2024, erişim tarihi Temmuz 20, 2025, [http://www.apsipa2024.org/files/papers/448.pdf](http://www.apsipa2024.org/files/papers/448.pdf)  
27. LLM OCR: why are they better than regular OCRs? \- Koncile, erişim tarihi Temmuz 20, 2025, [https://www.koncile.ai/en/ressources/why-llm-ocr-are-better-than-regular-ocrs](https://www.koncile.ai/en/ressources/why-llm-ocr-are-better-than-regular-ocrs)  
28. LLM vs OCR API: Cost Comparison for Document Processing in 2025 \- Mindee, erişim tarihi Temmuz 20, 2025, [https://www.mindee.com/blog/llm-vs-ocr-api-cost-comparison](https://www.mindee.com/blog/llm-vs-ocr-api-cost-comparison)  
29. How LLMs are Used to Extract Data from Documents? A Comprehensive Guide, erişim tarihi Temmuz 20, 2025, [https://www.documentpro.ai/blog/extract-data-from-documents-using-llms/](https://www.documentpro.ai/blog/extract-data-from-documents-using-llms/)  
30. How NER Identifies Key Financial Entities \- Phoenix Strategy Group, erişim tarihi Temmuz 20, 2025, [https://www.phoenixstrategy.group/blog/how-ner-identifies-key-financial-entities](https://www.phoenixstrategy.group/blog/how-ner-identifies-key-financial-entities)  
31. medium.com, erişim tarihi Temmuz 20, 2025, [https://medium.com/@kobigan.k/extracting-key-information-from-invoices-using-named-entity-recognition-ner-9c048efea90d\#:\~:text=Named%20Entity%20Recognition%20(NER)%20is,manual%20effort%2C%20enabling%20automated%20workflows.](https://medium.com/@kobigan.k/extracting-key-information-from-invoices-using-named-entity-recognition-ner-9c048efea90d#:~:text=Named%20Entity%20Recognition%20\(NER\)%20is,manual%20effort%2C%20enabling%20automated%20workflows.)  
32. What is Named Entity Recognition and How To Implement It? \- \- ThinkPalm, erişim tarihi Temmuz 20, 2025, [https://thinkpalm.com/blogs/what-is-named-entity-recognition-and-how-to-implement-it/](https://thinkpalm.com/blogs/what-is-named-entity-recognition-and-how-to-implement-it/)  
33. Human-in-the-Loop AI in Document Workflows \- Best Practices ..., erişim tarihi Temmuz 20, 2025, [https://parseur.com/blog/hitl-best-practices](https://parseur.com/blog/hitl-best-practices)  
34. Why AI still needs you: Exploring Human-in-the-Loop systems \- WorkOS, erişim tarihi Temmuz 20, 2025, [https://workos.com/blog/why-ai-still-needs-you-exploring-human-in-the-loop-systems](https://workos.com/blog/why-ai-still-needs-you-exploring-human-in-the-loop-systems)  
35. Human-In-The-Loop: What, How and Why | Devoteam, erişim tarihi Temmuz 20, 2025, [https://www.devoteam.com/expert-view/human-in-the-loop-what-how-and-why/](https://www.devoteam.com/expert-view/human-in-the-loop-what-how-and-why/)  
36. What is Continual Learning? \- IBM, erişim tarihi Temmuz 20, 2025, [https://www.ibm.com/think/topics/continual-learning](https://www.ibm.com/think/topics/continual-learning)  
37. Continual Learning in AI: How It Works & Why AI Needs It | Splunk, erişim tarihi Temmuz 20, 2025, [https://www.splunk.com/en\_us/blog/learn/continual-learning.html](https://www.splunk.com/en_us/blog/learn/continual-learning.html)  
38. Continuous Learning in Artificial Intelligence (AI) \- Leena AI, erişim tarihi Temmuz 20, 2025, [https://leena.ai/ai-glossary/continuous-learning](https://leena.ai/ai-glossary/continuous-learning)  
39. Scalable Document Processing \- Cirrus File Server, erişim tarihi Temmuz 20, 2025, [http://cirrusfileserver.com/scalable-document-processing](http://cirrusfileserver.com/scalable-document-processing)