# Testing the System
Now that we have everything ready, we can test the system. We will be simulating the following flow:

![overdue test flow](overdue-test-flow.svg)

So, we will be doing the following:
- Create an account

- Add default payment matching our test payment plugin

- Create a subscription

- Move the clock after the trial and observe first successful payment

- Configure payment plugin to fail payments

- Move the clock a month later and observe first failed payment

- Move clock +1 day and observe first payment retry

- Move clock +8 day and observe second payment retry

- Move clock +1 day and first overdue state WARNING

- Move clock +3 day and observe third payment retry

- Move clock +1 day and observe second overdue state BLOCKED

- Move clock +1 day and configure payment plugin to succeed

- Move clock +5 day (7 days from last payment attempt) and observe fourth 
payment retry which is successful

# Notes:

1. For simplicity, we are using dates (e.g 2021-01-10) when manipulating the Kill Bill clock instead of fully qualified datetimes (2021-01-10T01:43:23.000Z). Passing such a date will end up moving the Kill Bill clock to a given point in time and that point in time may end up before the exact time of the event we are trying to trigger. In such a case, retry moving the clock by one day and that should trigger it. An alternative is to specify the exact datetime when moving the clock. This would require retrieving the account object and obtaining the reference_time field from it to know the exact date time.

2. As you proceed with the steps below, you can verify each step by viewing the account in Kaui. The main account screen includes an OVERDUE STATUS field in the Billing Info section. The payment and invoices tab include information about payments and invoices. The Timeline tab within the account screen includes information about payment retries.

3. Start Kill Bill Ensure either on [AWS](https://docs.killbill.io/latest/getting_started#_aws_one_click), [Docker](https://docs.killbill.io/latest/getting_started#_docker), [Tomcat](https://docs.killbill.io/latest/getting_started#_tomcat) or in [standalone](https://docs.killbill.io/latest/development#_running_the_application) mode.

4. Set the date to 2021-07-26 (This is not mandatory, but would make the flow in sync with the diagram above):

```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H 'X-Killbill-CreatedBy: demo' \
-X POST \
"http://127.0.0.1:8080/1.0/kb/test/clock?requestedDate=2021-07-26"
```
5. Create your account:

```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H "X-Killbill-CreatedBy: demo" \
-X POST \
--data-binary '{"name":"Arthur","email":"arthur@laposte.fr","externalKey":"arthur","currency":"USD"}' \
"http://127.0.0.1:8080/1.0/kb/accounts"
```

6. Add the payment method (assuming 60035793-cbe5-472a-8bd8-3c67cc3beaf4 is the accountId):
```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H "X-Killbill-CreatedBy: demo" \
-X POST \
--data-binary '{"pluginName":"killbill-payment-test","pluginInfo":{}}' \
"http://127.0.0.1:8080/1.0/kb/accounts/60035793-cbe5-472a-8bd8-3c67cc3beaf4/paymentMethods?isDefault=true"
```

7. Create a subscription and verify that a $0 invoice is generated:
```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H "X-Killbill-CreatedBy: demo" \
-X POST \
--data-binary '{"accountId":"60035793-cbe5-472a-8bd8-3c67cc3beaf4","externalKey":"s1_arthur","productName":"Movies","productCategory":"BASE","billingPeriod":"MONTHLY","priceList":"DEFAULT"}' \
"http://127.0.0.1:8080/1.0/kb/subscriptions"
```
8. Move the clock to reach end of trial (2021-08-06) and see first payment:
```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H 'X-Killbill-CreatedBy: demo' \
-X POST \
"http://127.0.0.1:8080/1.0/kb/test/clock?requestedDate=2021-08-06"
```

9. Configure the payment plugin to fail subsequent payments (You can refer to the Payment Test Plugin Global State Configuration to understand this better).
```batch
curl -v \
-u'admin:password' \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H 'X-Killbill-CreatedBy: demo' \
-X POST \
--data-binary '{"CONFIGURE_ACTION":"ACTION_RETURN_PLUGIN_STATUS_ERROR", "METHODS":"purchasePayment"}' \
 -v 'http://127.0.0.1:8080/plugins/killbill-payment-test/configure'
```

10. Move the clock to the next month (2021-09-06) and observe first failed payment:
```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H 'X-Killbill-CreatedBy: demo' \
-X POST \
"http://127.0.0.1:8080/1.0/kb/test/clock?requestedDate=2021-09-06"
```

11. Move clock +1 day (2021-09-07) and observe first payment retry:
```batch
curl -v \
-u admin:password \
-H "X-Killbill-ApiKey: bob" \
-H "X-Killbill-ApiSecret: lazar" \
-H "Content-Type: application/json" \
-H 'X-Killbill-CreatedBy: demo' \
-X POST \
"http://127.0.0.1:8080/1.0/kb/test/clock?requestedDate=2021-09-07"
```

12. Move clock +8 day (2021-09-15) and observe second payment retry.

13. Move clock +1 day (2021-09-16) and verify that the account is in WARNING status.

14. Move clock +3 day (2021-09-19) and observe third payment retry.

15. Move clock +1 day (2021-09-20) and verify that the account is in BLOCKED status.

16. Move clock +1 day (2021-09-21) and configure the payment plugin to succeed:
```batch
curl -v \
-u'admin:password' \
-H "X-Killbill-ApiKey: bob" \
-H 'X-Killbill-ApiSecret: lazar' \
-H "Content-Type: application/json" \
-H 'X-Killbill-CreatedBy: demo' \
-X POST \
--data-binary '{"CONFIGURE_ACTION":"ACTION_CLEAR"}' \
 -v 'http://127.0.0.1:8080/plugins/killbill-payment-test/configure'
```

17. Move clock +5 day (2021-09-26) and observe the final payment retry. Verify that the payment is successful and the account is moved to the GOOD status.